# -*- coding: utf-8 -*--
# © 2022 Atingo Tadeusz Karpiński
# License OPL-1 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

import openerp
from openerp import models, api
from openerp.modules.module import get_test_modules, unwrap_suite, TestStream
import logging
import threading
import unittest2
import os
import unittest
import mock
import requests
import time
from openerp.tests.common import HOST
from openerp.tools.config import config

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
        thread = threading.Thread(target=openerp.service.server.start)
        thread.testing = True
        thread.start()
        time.sleep(6)
        requests.get("http://{host}:{port}/web".format(host=HOST, port=openerp.tools.config.get('http_port', '8069')))

        return thread

    @api.model
    def odoo_test_process_suites(self, suites):
        thread = False
        for suite in suites:
            if not thread and isinstance(suite[3], openerp.tests.common.HttpCase):
                with mock.patch("signal.signal", return_value=True):
                    thread = self.odoo_test_start_server()
        return suites

    @api.model
    def odoo_test_unwrap_tests(self, params):
        suites = []

        test_modules = params.test_modules
        test_module = params.test_module
        test_name = params.test_name
        test_class = params.test_class
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
            for m in mods:
                # tests = []
                for t in unwrap_suite(unittest.TestLoader().loadTestsFromModule(m)):
                    if self.match_test_filter(t, test_name, test_class):
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
            t0_sql = openerp.sql_db.sql_counter
            _logger.info("%s running tests.", name)
            result = unittest2.TextTestRunner(verbosity=2, stream=TestStream(name)).run(
                suite
            )
            if result.wasSuccessful():
                _logger.info(
                    "{name} tested in {time}, {sql_count} queries".format(name=name, time="{:.2f}".format((time.time() - t0)), sql_count=(openerp.sql_db.sql_counter - t0_sql))
                )
            if not result.wasSuccessful():
                r = False
                _logger.error(
                    "Module {test_module}: {failures} failures, {errors} errors".format(test_module=test_module, failures=len(result.failures), errors=len(result.errors))
                )

        return r
