# -*- coding: utf-8 -*--
# © 2022 Atingo Tadeusz Karpiński
# License OPL-1 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

import logging

from odoo import models, api
from odoo.addons.odoo_test_selenium.tests.odoo_test_selenium import (
    create_browser,
    SeleniumHttpCase,
)

_logger = logging.getLogger(__name__)


class IrModuleModule(models.Model):
    _inherit = "ir.module.module"

    @api.model
    def odoo_test_process_suites(self, suites):
        ctx = self._context.copy()
        suites = super(IrModuleModule, self).odoo_test_process_suites(suites)

        for suite in suites:
            if "test_selenium_example" in suite[1]:
                ctx["browser_visible"] = True

        browser = False
        for suite in suites:
            if not browser and isinstance(suite[3], SeleniumHttpCase):
                create_browser(ctx)

        return suites
