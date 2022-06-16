# -*- coding: utf-8 -*--
# © 2022 Atingo Tadeusz Karpiński
# License OPL-1 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

import logging
import argparse
import ast
import threading

import openerp
from openerp.tools.config import config
from openerp.cli import Command
from openerp.modules.module import load_information_from_description_file

_logger = logging.getLogger("Odoo Tests")

class Test(Command):
    """OdooTests Class"""

    def __init__(self):
        super(Test, self).__init__()

        self.parser = argparse.ArgumentParser(description="Odoo Tests")

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
            metavar="TEST_NAME",
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
            "--with-depends",
            action="store_true",
            default=False,
            help="With module/modules and all depends",
        )

    def run(self, args):
        self.params = self.parser.parse_args(args)

        try:
            self.params.parameters = ast.literal_eval(self.params.parameters)
        except:
            _logger.error(
                "{parameters} is not a dictionary. Parameters must be dict!".format(parameters=self.params.parameters)
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

        if self.params.with_depends and not self.params.test_modules:
            _logger.error(
                "--with-depends works only for module/modules tests !"
            )
            return

        if self.params.with_depends:
            module_depends = []
            for module in self.params.test_modules.split(","):
                module_info = load_information_from_description_file(module)
                module_info_depends = module_info.get("depends", [])
                for module_info_depend in module_info_depends:
                    module_depends.append(module_info_depend)
            module_depends = list(set(module_depends))
            self.params.test_modules = ",".join(module_depends)

        self.setup_env()

    def setup_env(self):
        threading.currentThread().testing = True
        with openerp.api.Environment.manage():
            if self.params.database:
                registry = openerp.registry(self.params.database)
                with registry.cursor() as cr:
                    uid = openerp.SUPERUSER_ID
                    ctx = openerp.api.Environment(cr, uid, {})["res.users"].context_get()
                    self.params.parameters.update(ctx)
                    env = openerp.api.Environment(cr, uid, self.params.parameters)
                    module_obj = env["ir.module.module"]
                    module_obj.odoo_tests_before()
                    try:
                        ok = True
                        suites = module_obj.odoo_tests_unwrap_tests(self.params)
                        suites = module_obj.odoo_tests_process_suites(suites)
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
                        module_obj.odoo_tests_after()
            else:
                _logger.error("Select database with --database")
