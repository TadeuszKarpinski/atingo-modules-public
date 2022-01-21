# -*- coding: utf-8 -*--
# © 2022 Atingo Tadeusz Karpiński
# License AGPL-3.0 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

import logging
import argparse

import odoo
from odoo.tools.config import config
from odoo.cli import Command

_logger = logging.getLogger("Odoo Command")


def with_env(func):
    def setup_env(self, *args, **kwargs):
        with odoo.api.Environment.manage():
            if self.params.database:
                registry = odoo.registry(self.params.database)
                with registry.cursor() as cr:
                    uid = odoo.SUPERUSER_ID
                    ctx = odoo.api.Environment(cr, uid, {})["res.users"].context_get()
                    env = odoo.api.Environment(cr, uid, ctx)
                    self.env = env
                    func(self, *args, **kwargs)
    return setup_env


class OdooCommand(Command):
    """OdooCommand Class"""

    def __init__(self):
        super(OdooCommand, self).__init__()

        self.parser = argparse.ArgumentParser(description="Odoo Command")

        self.parser.add_argument(
            "--list",
            dest="list",
            default=False,
            action="store_true",
            help="Update list of modules",
        )
        self.parser.add_argument(
            "--database",
            dest="database",
            default=None,
            help="Specify the database name",
        )
        self.parser.add_argument(
            "--module",
            metavar="MODULE",
            required=False,
            help="Specify module",
        )
        self.parser.add_argument(
            "--modules",
            metavar="MODULES",
            required=False,
            help="Specify modules",
        )

    def run(self, args):
        self.params = self.parser.parse_args(args)

        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
        )

        self.modules_list = []

        if not self.params.database:
            self.params.database = config.get("db_name", False)

        if not self.params.database:
            _logger.error("Select database with --database")
            return

        if self.params.module and not self.params.modules:
            self.params.modules = self.params.module

        self.pre_run()
        self.run_command()

    @with_env
    def pre_run(self):
        if self.params.list:
            _logger.info("Update list of modules")
            self.env["ir.module.module"].update_list()

        if self.params.modules:
            for module in self.params.modules.split(","):
                self.modules_list.append(module)
            self.modules_list = list(set(self.modules_list))

    def run_command(self):
        pass