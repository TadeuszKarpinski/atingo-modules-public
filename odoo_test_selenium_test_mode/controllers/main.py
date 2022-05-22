# -*- coding: utf-8 -*--
# © 2022 Atingo Tadeusz Karpiński
# License OPL-1 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

import unittest
import unittest2
import logging

from odoo.modules.module import TestStream
from odoo import http
from odoo.http import request
from odoo.addons.odoo_test_selenium_test_mode.tests.odoo_test_selenium_test_mode import (
    OdooTestSeleniumTestModeTransactionCase,
)

_logger = logging.getLogger(__name__)


class TestSeleniumTestMode(http.Controller):
    @http.route("/enter_test_mode", type="http", auth="user")
    def enter_test_mode(self):
        param = (
            request.env["ir.config_parameter"]
            .sudo()
            .get_param("odoo_test_selenium_test_mode.test_mode")
        )
        if param == "False":
            request.env["ir.config_parameter"].sudo().set_param(
                "odoo_test_selenium_test_mode.test_mode", "True"
            )
            t = unittest.TestLoader().loadTestsFromTestCase(
                OdooTestSeleniumTestModeTransactionCase
            )
            suite = unittest.TestSuite([t])
            unittest2.TextTestRunner(verbosity=2, stream=TestStream("odoo_test_selenium_test_mode")).run(suite)
            self.odoo_test_mode_notification(
                "odoo_test_selenium_test_mode", "leave_test_mode"
            )
        return "ok"

    @http.route("/leave_test_mode", type="http", auth="user")
    def leave_test_mode(self):
        param = (
            request.env["ir.config_parameter"]
            .sudo()
            .get_param("odoo_test_selenium_test_mode.test_mode")
        )
        if param == "True":
            request.env["ir.config_parameter"].sudo().set_param(
                "odoo_test_selenium_test_mode.test_mode", "False"
            )
        return "ok"

    @http.route("/odoo_test_mode_notification", type="json", auth="user")
    def odoo_test_mode_notification(self, channel, message):
        return request.env["bus.bus"].sendmany([(channel, message)])
