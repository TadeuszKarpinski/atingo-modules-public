# -*- coding: utf-8 -*--
# © 2022 Atingo Tadeusz Karpiński
# License AGPL-3.0 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

from openerp import models, api, _


class ir_model(models.Model):
    _inherit = "ir.model"

    def action_show_records(self, cr, uid, ids, context=None):
        model = self.browse(cr, uid, ids, context=context)[0]
        return {
            "display_name": model.name,
            "name": model.name,
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "tree,form",
            "res_model": model.model,
            "views": [],
            "view_id": [],
            "target": "current",
            "context": context,
        }
