# -*- coding: utf-8 -*--
# © 2022 Atingo Tadeusz Karpiński
# License AGPL-3.0 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

import logging
import datetime

from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class Employee(models.Model):
    _inherit = "hr.employee"

    send_birthday_reminders = fields.Boolean("Include in Birthday Reminder List")
    birthday_remind_date = fields.Date("Birthday Remind Date", compute="_compute_birthday_reminder_dates", search="_search_birthday_remind_date", readonly=True)
    next_birthday_date = fields.Date("Next Birthday", compute="_compute_birthday_reminder_dates", search="_search_next_birthday_date", readonly=True)

    def _search_birthday_remind_date(self, operator, value):
        if not value:
            return [('birthday', operator, value)]

        employees = self.search([("birthday", '!=', False), ("send_birthday_reminders", "=", True)])
        employees.refresh()
        if operator == "=":
            return [("id", "in", employees.filtered(lambda employee: employee.birthday_remind_date == value).ids)]
        if operator == "!=":
            return [("id", "in", employees.filtered(lambda employee: employee.birthday_remind_date != value).ids)]
        if operator == ">":
            return [("id", "in", employees.filtered(lambda employee: employee.birthday_remind_date > value).ids)]
        if operator == ">=":
            return [("id", "in", employees.filtered(lambda employee: employee.birthday_remind_date >= value).ids)]
        if operator == "<":
            return [("id", "in", employees.filtered(lambda employee: employee.birthday_remind_date < value).ids)]
        if operator == "<=":
            return [("id", "in", employees.filtered(lambda employee: employee.birthday_remind_date <= value).ids)]

    def _search_next_birthday_date(self, operator, value):
        if not value:
            return [('birthday', operator, value)]

        employees = self.search([("birthday", '!=', False), ("send_birthday_reminders", "=", True)])
        employees.refresh()
        if operator == "=":
            return [("id", "in", employees.filtered(lambda employee: employee.next_birthday_date == value).ids)]
        if operator == "!=":
            return [("id", "in", employees.filtered(lambda employee: employee.next_birthday_date != value).ids)]
        if operator == ">":
            return [("id", "in", employees.filtered(lambda employee: employee.next_birthday_date > value).ids)]
        if operator == ">=":
            return [("id", "in", employees.filtered(lambda employee: employee.next_birthday_date >= value).ids)]
        if operator == "<":
            return [("id", "in", employees.filtered(lambda employee: employee.next_birthday_date < value).ids)]
        if operator == "<=":
            return [("id", "in", employees.filtered(lambda employee: employee.next_birthday_date <= value).ids)]

    @api.depends('birthday')
    def _compute_birthday_reminder_dates(self):
        today = fields.Date.today()
        today_datetime = datetime.datetime.strptime(today, '%Y-%m-%d')
        employees_with_birthday_reminder = self.filtered(lambda employee: employee.birthday != False and employee.send_birthday_reminders == True)

        for employee in employees_with_birthday_reminder:
            notify_threshold = employee.department_id and employee.department_id.birthday_reminder_threshold_days or 0
            birthday_datetime = datetime.datetime.strptime(employee.birthday, '%Y-%m-%d')
            next_birthday_datetime = birthday_datetime.replace(year=today_datetime.year)

            if next_birthday_datetime < birthday_datetime:  # employee wasn't born yet :P
                employee.next_birthday_date = birthday_datetime
                employee.birthday_remind_date = birthday_datetime - datetime.timedelta(days=notify_threshold)
            elif next_birthday_datetime <= today_datetime:  # employee already had birthday
                next_birthday_datetime = next_birthday_datetime.replace(year=next_birthday_datetime.year+1)
                employee.next_birthday_date = next_birthday_datetime
                employee.birthday_remind_date = next_birthday_datetime - datetime.timedelta(days=notify_threshold)
            else:  # employee will have birthday
                employee.next_birthday_date = next_birthday_datetime
                employee.birthday_remind_date = next_birthday_datetime - datetime.timedelta(days=notify_threshold)

        (self - employees_with_birthday_reminder).write({
            "birthday_remind_date": False,
            "next_birthday_date": False,
        })

    @api.multi
    def send_birthday_reminder_email(self):
        template = self.env.ref("odoo_birthday_reminder.email_birthday_reminder")
        res_partner_obj = self.env["res.partner"]
        for employee in self:
            partners = res_partner_obj
            if employee.department_id:
                partners = employee.department_id.birthday_reminder_recipient_ids
            if employee.user_id and employee.user_id.partner_id:
                partners = partners - employee.user_id.partner_id

            for partner in partners:
                email_values={'partner_to': [partner.id], "lang": partner.lang}
                template.send_mail(employee.id, email_values=email_values)

    @api.model
    def process_birthday_reminders(self):
        today = fields.Date.today()
        employees = self.search([("birthday_remind_date", "<=", today)])
        employees.send_birthday_reminder_email()