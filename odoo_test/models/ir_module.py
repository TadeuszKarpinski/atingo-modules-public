# -*- coding: utf-8 -*--
# © 2022 Atingo Tadeusz Karpiński
# License OPL-1 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

import odoo
from odoo import models, api
from odoo.modules.module import get_test_modules, unwrap_suite, TestStream
import logging
import threading
import unittest2
import os
import unittest
import requests
import time
from odoo.tests.common import HOST

_logger = logging.getLogger(__name__)


class IrModuleModule(models.Model):
    _inherit = "ir.module.module"

    @api.model
    def odoo_test_before(self):
        pass

    @api.model
    def odoo_test_after(self):
        os._exit(1)

    @api.model
    def match_test_filter(self, test, test_name, test_class):
        if not test_name or not isinstance(test, unittest.TestCase):
            if not test_class:
                return True
            return type(test).__name__ == test_class
        return test._testMethodName == test_name

    @api.model
    def odoo_test_start_server(self):
        _logger.info("Start odoo server for tests")
        self = self.with_context(odoo_test_server_started=True)
        thread = threading.Thread(target=odoo.service.server.start)
        thread.testing = True
        thread.start()
        time.sleep(6)
        requests.get(f"http://{HOST}:{odoo.tools.config.get('http_port', '8069')}/web")

        return thread

    @api.model
    def odoo_test_process_suites(self, suites):
        thread = False
        for suite in suites:
            if not thread and isinstance(suite[3], odoo.tests.common.HttpCase):
                with unittest.mock.patch("signal.signal", return_value=True):
                    thread = self.odoo_test_start_server()
        return suites

    @api.model
    def odoo_test_unwrap_tests(self, params):
        from odoo.tests.common import TagsSelector

        suites = []

        test_modules = params.test_modules
        test_module = params.test_module
        test_name = params.test_name
        test_class = params.test_class
        test_tags = params.test_tags
        test_position = params.test_position
        cr = self.env.cr

        test_modules_list = []

        if test_module and not test_modules:
            test_modules = test_module

        if test_modules:
            for test_module in test_modules.split(","):
                test_modules_list.append(test_module.strip())

        if not test_modules_list:
            cr.execute("SELECT name from ir_module_module WHERE state = 'installed' ")
            test_modules_list = [name for (name,) in cr.fetchall()]

        for test_module in test_modules_list:
            mods = get_test_modules(test_module)
            config_tags = TagsSelector(test_tags) if test_tags else None
            position_tag = TagsSelector(test_position) if test_position else None
            for m in mods:
                # tests = []
                for t in unwrap_suite(unittest.TestLoader().loadTestsFromModule(m)):
                    if (
                        (not position_tag or position_tag.check(t))
                        and (not config_tags or config_tags.check(t))
                        and self.match_test_filter(t, test_name, test_class)
                    ):
                        suite = unittest.TestSuite([t])
                        suites.append([test_module, m.__name__, suite, t])

        if not suites:
            _logger.error("No tests to start !")

        return suites

    @api.model
    def run_test(self, test_module, name, suite, test):
        r = True

        suite = unittest.TestSuite(suite)
        if suite.countTestCases():
            t0 = time.time()
            t0_sql = odoo.sql_db.sql_counter
            _logger.info("%s running tests.", name)
            result = unittest2.TextTestRunner(verbosity=2, stream=TestStream(name)).run(suite)
            if result.wasSuccessful():
                _logger.info(
                    f"{name} tested in {(time.time() - t0):.2f}, {odoo.sql_db.sql_counter - t0_sql} queries"
                )
            if not result.wasSuccessful():
                r = False
                _logger.error(
                    f"Module {test_module}: {len(result.failures)} failures, {len(result.errors)} errors"
                )

        return r
