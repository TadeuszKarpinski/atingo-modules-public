# -*- coding: utf-8 -*--
# © 2021 PwC (Krzysztof Grabarczyk, Filip Karpiński, Tadeusz Karpiński)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = "res.users"

    def create(self, vals):
        vals[0].pop("image_1920", None)
        vals = self.env["res.partner"].get_new_avatar(vals[0])
        users = super().create(vals)
        return users