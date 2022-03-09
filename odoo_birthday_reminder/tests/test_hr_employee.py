# -*- coding: utf-8 -*--
# © 2022 Atingo Tadeusz Karpiński
# License AGPL-3.0 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

import datetime
import mock

from odoo.tests.common import TransactionCase
from odoo import fields


class TestOdooBirthdayReminderHrEmployee(TransactionCase):

    def setUp(self):
        super(TestOdooBirthdayReminderHrEmployee, self).setUp()

        self.today = fields.Date.today()
        self.hr_employee_obj = self.env["hr.employee"]
        self.hr_department_obj = self.env["hr.department"]
        self.mail_mail_obj = self.env["mail.mail"]
        self.res_partner_obj = self.env["res.partner"]
        self.res_users_obj = self.env["res.users"]

    def test_simple(self):
        employee = self.hr_employee_obj.create({"name": "Test Employee"})

        # fields should be empty for newly created employees
        self.assertEqual(False, employee.send_birthday_reminders)
        self.assertEqual(False, employee.birthday_remind_date)
        self.assertEqual(False, employee.next_birthday_date)

        # set birthday date, fields should be empty
        employee.birthday = self.today
        employee.refresh()
        self.assertEqual(False, employee.send_birthday_reminders)
        self.assertEqual(False, employee.birthday_remind_date)
        self.assertEqual(False, employee.next_birthday_date)

        # set birthday reminders, fields shouldnt be empty
        employee.send_birthday_reminders = True
        employee.refresh()
        self.assertEqual(True, employee.send_birthday_reminders)
        self.assertNotEqual(False, employee.birthday_remind_date)
        self.assertNotEqual(False, employee.next_birthday_date)

    @mock.patch(
        "odoo.fields.Date.today",
        return_value="2137-04-02",
    )
    def test_next_birthday_date(self, *args):
        employee = self.hr_employee_obj.create({"name": "Test Employee"})

        # birthday is empty by default
        self.assertEqual(False, employee.birthday)
        self.assertEqual(False, employee.next_birthday_date)
        self.assertEqual(False, employee.send_birthday_reminders)
        self.assertEqual(False, employee.birthday_remind_date)

        # set birthday for far future, no reminders
        employee.birthday = "2200-01-01"
        employee.refresh()
        self.assertEqual("2200-01-01", employee.birthday)
        self.assertEqual(False, employee.next_birthday_date)
        self.assertEqual(False, employee.send_birthday_reminders)
        self.assertEqual(False, employee.birthday_remind_date)

        # set reminders
        employee.send_birthday_reminders = True
        employee.refresh()
        self.assertEqual("2200-01-01", employee.birthday)
        self.assertEqual("2200-01-01", employee.next_birthday_date)
        self.assertEqual(True, employee.send_birthday_reminders)
        self.assertEqual("2200-01-01", employee.birthday_remind_date)

        # set birthday far past (birthday already was in this year)
        employee.birthday = "1900-01-01"
        employee.refresh()
        self.assertEqual("1900-01-01", employee.birthday)
        self.assertEqual("2138-01-01", employee.next_birthday_date)
        self.assertEqual(True, employee.send_birthday_reminders)
        self.assertEqual("2138-01-01", employee.birthday_remind_date)

        # set birthday far past (birthday will be in this year)
        employee.birthday = "1900-12-31"
        employee.refresh()
        self.assertEqual("1900-12-31", employee.birthday)
        self.assertEqual("2137-12-31", employee.next_birthday_date)
        self.assertEqual(True, employee.send_birthday_reminders)
        self.assertEqual("2137-12-31", employee.birthday_remind_date)

        # set birthday XXXX-04-02 (today)
        employee.birthday = "1991-04-02"
        employee.refresh()
        self.assertEqual("1991-04-02", employee.birthday)
        self.assertEqual("2138-04-02", employee.next_birthday_date)
        self.assertEqual(True, employee.send_birthday_reminders)
        self.assertEqual("2138-04-02", employee.birthday_remind_date)

        # set birthday XXXX-04-03 (tomorrow)
        employee.birthday = "1991-04-03"
        employee.refresh()
        self.assertEqual("1991-04-03", employee.birthday)
        self.assertEqual("2137-04-03", employee.next_birthday_date)
        self.assertEqual(True, employee.send_birthday_reminders)
        self.assertEqual("2137-04-03", employee.birthday_remind_date)

        # set birthday XXXX-04-01 (yesterday)
        employee.birthday = "1991-04-01"
        employee.refresh()
        self.assertEqual("1991-04-01", employee.birthday)
        self.assertEqual("2138-04-01", employee.next_birthday_date)
        self.assertEqual(True, employee.send_birthday_reminders)
        self.assertEqual("2138-04-01", employee.birthday_remind_date)

    @mock.patch(
        "odoo.fields.Date.today",
        return_value="2137-04-02",
    )
    def test_birthday_remind_date(self, *args):
        department = self.hr_department_obj.create({"name": "Test Department"})
        employee = self.hr_employee_obj.create({"name": "Test Employee", "department_id": department.id,})

        # birthday is empty by default
        self.assertEqual(False, employee.birthday)
        self.assertEqual(False, employee.next_birthday_date)
        self.assertEqual(False, employee.send_birthday_reminders)
        self.assertEqual(False, employee.birthday_remind_date)

        # set birthday for far future, no reminders
        employee.birthday = "2200-01-01"
        employee.refresh()
        self.assertEqual("2200-01-01", employee.birthday)
        self.assertEqual(False, employee.next_birthday_date)
        self.assertEqual(False, employee.send_birthday_reminders)
        self.assertEqual(False, employee.birthday_remind_date)

        # set reminders
        employee.send_birthday_reminders = True
        employee.refresh()
        self.assertEqual("2200-01-01", employee.birthday_remind_date)
        department.birthday_reminder_threshold_days = 10
        employee.refresh()
        self.assertEqual("2199-12-22", employee.birthday_remind_date)
        department.birthday_reminder_threshold_days = 0

        # set birthday far past (birthday already was in this year)
        employee.birthday = "1900-01-01"
        employee.refresh()
        self.assertEqual("2138-01-01", employee.birthday_remind_date)
        department.birthday_reminder_threshold_days = 20
        employee.refresh()
        self.assertEqual("2137-12-12", employee.birthday_remind_date)
        department.birthday_reminder_threshold_days = 0

        # set birthday far past (birthday will be in this year)
        employee.birthday = "1900-12-31"
        employee.refresh()
        self.assertEqual("2137-12-31", employee.birthday_remind_date)
        department.birthday_reminder_threshold_days = 30
        employee.refresh()
        self.assertEqual("2137-12-01", employee.birthday_remind_date)
        department.birthday_reminder_threshold_days = 0

        # set birthday XXXX-04-02 (today)
        employee.birthday = "1991-04-02"
        employee.refresh()
        self.assertEqual("2138-04-02", employee.birthday_remind_date)
        department.birthday_reminder_threshold_days = 33
        employee.refresh()
        self.assertEqual("2138-02-28", employee.birthday_remind_date)
        department.birthday_reminder_threshold_days = 0

        # set birthday XXXX-04-03 (tomorrow)
        employee.birthday = "1991-04-03"
        employee.refresh()
        self.assertEqual("2137-04-03", employee.birthday_remind_date)
        department.birthday_reminder_threshold_days = 27
        employee.refresh()
        self.assertEqual("2137-03-07", employee.birthday_remind_date)
        department.birthday_reminder_threshold_days = 0

        # set birthday XXXX-04-01 (yesterday)
        employee.birthday = "1991-04-01"
        employee.refresh()
        self.assertEqual("2138-04-01", employee.birthday_remind_date)
        department.birthday_reminder_threshold_days = 1
        employee.refresh()
        self.assertEqual("2138-03-31", employee.birthday_remind_date)
        department.birthday_reminder_threshold_days = 0

    @mock.patch(
        "odoo.fields.Date.today",
        return_value="2137-04-02",
    )
    def test_many_employees_compute(self, *args):
        existing_employees = self.hr_employee_obj.search([])
        employee1 = self.hr_employee_obj.create({
            "name": "Test Employee 1",
            "send_birthday_reminders": True,
        })
        employee2 = self.hr_employee_obj.create({
            "name": "Test Employee 2",
            "send_birthday_reminders": True,
        })
        employee3 = self.hr_employee_obj.create({
            "name": "Test Employee 3",
            "send_birthday_reminders": True,
            "birthday": "1991-01-16",
        })
        employee4 = self.hr_employee_obj.create({
            "name": "Test Employee 4",
            "send_birthday_reminders": True,
            "birthday": "2991-01-16",
        })
        new_employees = self.hr_employee_obj.search([]) - existing_employees
        new_employees.refresh()

        self.assertEqual(False, employee1.next_birthday_date)
        self.assertEqual(False, employee1.birthday_remind_date)
        self.assertEqual(False, employee2.next_birthday_date)
        self.assertEqual(False, employee2.birthday_remind_date)
        self.assertEqual("2138-01-16", employee3.next_birthday_date)
        self.assertEqual("2138-01-16", employee3.birthday_remind_date)
        self.assertEqual("2991-01-16", employee4.next_birthday_date)
        self.assertEqual("2991-01-16", employee4.birthday_remind_date)

    @mock.patch(
        "odoo.fields.Date.today",
        return_value="2137-04-02",
    )
    def test_birthday_remind_date_search(self, *args):
        department = self.hr_department_obj.create({"name": "Test Department", "birthday_reminder_threshold_days": 1})
        employee = self.hr_employee_obj.create({
            "name": "Test Employee",
            "send_birthday_reminders": True,
            "birthday": "1991-01-17",
            "department_id": department.id,
        })

        # case =
        employees = self.hr_employee_obj.search([("birthday_remind_date", "=", "2138-01-16")])
        self.assertIn(employee, employees)

        employees = self.hr_employee_obj.search([("birthday_remind_date", "=", "2138-01-07")])
        self.assertNotIn(employee, employees)

        # case !=
        employees = self.hr_employee_obj.search([("birthday_remind_date", "!=", "2138-01-16")])
        self.assertNotIn(employee, employees)

        employees = self.hr_employee_obj.search([("birthday_remind_date", "!=", "2138-01-07")])
        self.assertIn(employee, employees)
        
        # case >
        employees = self.hr_employee_obj.search([("birthday_remind_date", ">", "2138-01-16")])
        self.assertNotIn(employee, employees)

        employees = self.hr_employee_obj.search([("birthday_remind_date", ">", "2138-01-07")])
        self.assertIn(employee, employees)

        # case >=
        employees = self.hr_employee_obj.search([("birthday_remind_date", ">=", "2138-01-16")])
        self.assertIn(employee, employees)

        employees = self.hr_employee_obj.search([("birthday_remind_date", ">=", "2138-01-07")])
        self.assertIn(employee, employees)

        # case <
        employees = self.hr_employee_obj.search([("birthday_remind_date", "<", "2138-01-16")])
        self.assertNotIn(employee, employees)

        employees = self.hr_employee_obj.search([("birthday_remind_date", "<", "2138-01-07")])
        self.assertNotIn(employee, employees)

        # case <=
        employees = self.hr_employee_obj.search([("birthday_remind_date", "<=", "2138-01-16")])
        self.assertIn(employee, employees)

        employees = self.hr_employee_obj.search([("birthday_remind_date", "<=", "2138-01-07")])
        self.assertNotIn(employee, employees)

    @mock.patch(
        "odoo.fields.Date.today",
        return_value="2137-04-02",
    )
    def testnext_birthday_date_search(self, *args):
        employee = self.hr_employee_obj.create({
            "name": "Test Employee",
            "send_birthday_reminders": True,
            "birthday": "1991-01-16",
        })

        # case =
        employees = self.hr_employee_obj.search([("next_birthday_date", "=", "2138-01-16")])
        self.assertIn(employee, employees)

        employees = self.hr_employee_obj.search([("next_birthday_date", "=", "2138-01-07")])
        self.assertNotIn(employee, employees)

        # case !=
        employees = self.hr_employee_obj.search([("next_birthday_date", "!=", "2138-01-16")])
        self.assertNotIn(employee, employees)

        employees = self.hr_employee_obj.search([("next_birthday_date", "!=", "2138-01-07")])
        self.assertIn(employee, employees)
        
        # case >
        employees = self.hr_employee_obj.search([("next_birthday_date", ">", "2138-01-16")])
        self.assertNotIn(employee, employees)

        employees = self.hr_employee_obj.search([("next_birthday_date", ">", "2138-01-07")])
        self.assertIn(employee, employees)

        # case >=
        employees = self.hr_employee_obj.search([("next_birthday_date", ">=", "2138-01-16")])
        self.assertIn(employee, employees)

        employees = self.hr_employee_obj.search([("next_birthday_date", ">=", "2138-01-07")])
        self.assertIn(employee, employees)

        # case <
        employees = self.hr_employee_obj.search([("next_birthday_date", "<", "2138-01-16")])
        self.assertNotIn(employee, employees)

        employees = self.hr_employee_obj.search([("next_birthday_date", "<", "2138-01-07")])
        self.assertNotIn(employee, employees)

        # case <=
        employees = self.hr_employee_obj.search([("next_birthday_date", "<=", "2138-01-16")])
        self.assertIn(employee, employees)

        employees = self.hr_employee_obj.search([("next_birthday_date", "<=", "2138-01-07")])
        self.assertNotIn(employee, employees)

    def test_send_birthday_reminder_email_simple(self):
        emails_count = self.mail_mail_obj.search_count([])

        employee = self.hr_employee_obj.create({
            "name": "Test Employee",
            "send_birthday_reminders": True,
            "birthday": "1991-01-16",
        })
        employee.send_birthday_reminder_email()
        emails_count2 = self.mail_mail_obj.search_count([])

        # email wasnt sent
        self.assertEqual(emails_count, emails_count2)

        partner = self.res_partner_obj.create({"name": "Test Partner"})
        department = self.hr_department_obj.create({
            "name": "Test Department", 
            "birthday_reminder_threshold_days": 1,
            "birthday_reminder_recipient_ids": [(6, 0, [partner.id])],
        })
        employee.department_id = department

        employee.send_birthday_reminder_email()

        emails_count3 = self.mail_mail_obj.search_count([])

        self.assertEqual(emails_count+1, emails_count3)

    def test_send_birthday_reminder_email_to_partner(self):
        emails_count = self.mail_mail_obj.search_count([])

        user = self.res_users_obj.create({"name": "Test User", "login": "test.email@example.com"})
        department = self.hr_department_obj.create({
            "name": "Test Department", 
            "birthday_reminder_threshold_days": 1,
            "birthday_reminder_recipient_ids": [(6, 0, [user.partner_id.id])],
        })
        employee = self.hr_employee_obj.create({
            "name": "Test Employee",
            "send_birthday_reminders": True,
            "birthday": "1991-01-16",
            "user_id": user.id,
            "department_id": department.id,
        })
        employee.send_birthday_reminder_email()
        emails_count2 = self.mail_mail_obj.search_count([])

        self.assertEqual(emails_count, emails_count2)

    @mock.patch(
        "odoo.fields.Date.today",
        return_value="2137-04-02",
    )
    def test_birthday_reminder_cron(self, *args):
        cron = self.env.ref("odoo_birthday_reminder.ir_cron_birthday_reminder_scheduler_action")

        emails_count = self.mail_mail_obj.search_count([])

        partner1 = self.res_partner_obj.create({"name": "Test Partner"})
        partner2 = self.res_partner_obj.create({"name": "Test Partner 2"})
        user = self.res_users_obj.create({"name": "Test User", "login": "test.email@example.com"})
        department = self.hr_department_obj.create({
            "name": "Test Department", 
            "birthday_reminder_threshold_days": 1,
            "birthday_reminder_recipient_ids": [(6, 0, [user.partner_id.id, partner1.id, partner2.id])],
        })
        employee = self.hr_employee_obj.create({
            "name": "Test Employee",
            "send_birthday_reminders": True,
            "birthday": "1991-04-03",
            "user_id": user.id,
            "department_id": department.id,
        })

        cron.method_direct_trigger()

        emails_count2 = self.mail_mail_obj.search_count([])

        self.assertEqual(emails_count+2, emails_count2)


