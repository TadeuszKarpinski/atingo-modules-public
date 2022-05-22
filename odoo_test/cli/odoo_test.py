# -*- coding: utf-8 -*--
# © 2022 Atingo Tadeusz Karpiński
# License OPL-1 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

import logging
import argparse
import ast
import threading

import odoo
from odoo.tools.config import config
from odoo.cli import Command

_logger = logging.getLogger("Odoo Test")


class Test(Command):
    """OdooTest Class"""

    def __init__(self):
        super(Test, self).__init__()

        self.parser = argparse.ArgumentParser(description="Odoo Test")

        self.parser.add_argument(
            "--parameters",
            dest="parameters",
            default="{}",
            help="Specify parameters in dictionary",
        )
        self.parser.add_argument(
            "--database",
            dest="database",
            default=None,
            help="Specify the database name",
        )
        self.parser.add_argument(
            "--test-name",
            metavar="TEST_Name",
            required=False,
            help="Specify the test method name",
        )
        self.parser.add_argument(
            "--test-class",
            metavar="TEST_CLASS",
            required=False,
            help="Specify the test class",
        )
        self.parser.add_argument(
            "--test-module",
            metavar="TEST_MODULE",
            required=False,
            help="Specify module to test",
        )
        self.parser.add_argument(
            "--test-modules",
            metavar="TEST_MODULES",
            required=False,
            help="Specify modules to test",
        )
        self.parser.add_argument(
            "--test-download",
            metavar="TEST_DOWNLOAD",
            required=False,
            help="Specify test download diretory (e.g. for reports)",
        )
        self.parser.add_argument(
            "--test-tags", metavar="TEST_TAGS", required=False, help="Specify test tags"
        )
        self.parser.add_argument(
            "--test-position",
            metavar="TEST_POSITION",
            required=False,
            help="Specify position tags: post_install, at_install",
        )

    def run(self, args):
        self.params = self.parser.parse_args(args)

        try:
            self.params.parameters = ast.literal_eval(self.params.parameters)
        except:
            _logger.error(
                f"{self.params.parameters} is not a dictionary. Parameters must be dict!"
            )
            return

        config["testing"] = True

        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
        )

        if not self.params.database:
            self.params.database = config.get("db_name", False)

        if self.params.test_module and not self.params.test_modules:
            self.params.test_modules = self.params.test_module

        self.setup_env()

    def setup_env(self):
        threading.currentThread().testing = True
        with odoo.api.Environment.manage():
            if self.params.database:
                registry = odoo.registry(self.params.database)
                with registry.cursor() as cr:
                    uid = odoo.SUPERUSER_ID
                    ctx = odoo.api.Environment(cr, uid, {})["res.users"].context_get()
                    self.params.parameters.update(ctx)
                    env = odoo.api.Environment(cr, uid, self.params.parameters)
                    module_obj = env["ir.module.module"]
                    module_obj.odoo_test_before()
                    try:
                        ok = True
                        suites = module_obj.odoo_test_unwrap_tests(self.params)
                        suites = module_obj.odoo_test_process_suites(suites)
                        for suite in suites:
                            ok = module_obj.run_test(*suite) and ok
                        if ok:
                            _logger.info("Finished!")
                        else:
                            _logger.info("Tests Failed!")

                    except Exception as e:
                        _logger.exception(e)
                    finally:
                        cr.rollback()
                        module_obj.odoo_test_after()
            else:
                _logger.error("Select database with --database")
