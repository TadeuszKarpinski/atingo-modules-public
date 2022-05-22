# -*- coding: utf-8 -*--
# © 2022 Atingo Tadeusz Karpiński
# License OPL-1 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

import logging
import time

from odoo.tests.common import HttpCase

_logger = logging.getLogger(__name__)


class TestOdooTestSeleniumTestModeTransactionCase(HttpCase):
    def test_enter_test_mode(self):
        self.env["ir.config_parameter"].sudo().set_param(
            "odoo_test_selenium_test_mode.test_mode", "True"
        )
        _logger.warning("Database {dbname} is entering Test Mode !".format(dbname=self.cr.dbname))
        counter = 0

        for i in range(1, 1200):
            counter = counter + 1
            if counter >= 10:
                _logger.warning("Database {dbname} is in Test Mode !".format(dbname=self.cr.dbname))
                counter = 0
            param = (
                self.env["ir.config_parameter"]
                .sudo()
                .get_param("odoo_test_selenium_test_mode.test_mode")
            )
            if param == "False":
                _logger.warning("Database {dbname} is leaving Test Mode !".format(dbname=self.cr.dbname))
                return
            time.sleep(1)
        _logger.warning("Database {dbname} is leaving Test Mode !".format(dbname=self.cr.dbname))
