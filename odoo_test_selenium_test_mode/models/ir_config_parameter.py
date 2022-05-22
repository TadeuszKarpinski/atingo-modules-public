# -*- coding: utf-8 -*--
# © 2022 Atingo Tadeusz Karpiński
# License OPL-1 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

import logging

from odoo import models, api, SUPERUSER_ID

_logger = logging.getLogger(__name__)


class IrConfigParameter(models.Model):
    _inherit = "ir.config_parameter"

    @api.model
    def get_odoo_test_selenium_test_mode(self):
        return self.with_user(SUPERUSER_ID).get_param(
            "odoo_test_selenium_test_mode.test_mode"
        )
