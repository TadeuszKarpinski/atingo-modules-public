# -*- coding: utf-8 -*--
# © 2022 Atingo Tadeusz Karpiński
# License AGPL-3.0 (https://www.odoo.com/documentation/15.0/legal/licenses.html).


from odoo import models, fields

class Department(models.Model):
    _inherit = "hr.department"

    birthday_reminder_threshold_days = fields.Integer("Birthday Threshold (days)", default=0)
    birthday_reminder_recipient_ids = fields.Many2many('res.partner', 'birthday_reminder_res_partner_hr_department_rel', 'partner_id', 'department_id', string='Birthday Reminder Recipients')
