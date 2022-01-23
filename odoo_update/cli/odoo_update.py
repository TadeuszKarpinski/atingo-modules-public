# -*- coding: utf-8 -*--
# © 2022 Atingo Tadeusz Karpiński
# License AGPL-3.0 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

import logging
import sys

import openerp
from openerp.tools.config import config
from openerp.modules.module import load_information_from_description_file
from .odoo_command import OdooCommand, with_env 

_logger = logging.getLogger("Odoo Update")


class Update(OdooCommand):
    """Update Class"""

    def __init__(self):
        super(Update, self).__init__()

        self.parser.add_argument(
            "--with-depends",
            action="store_true",
            default=False,
            help="Update with depends of modules",
        )
        self.parser.add_argument(
            "--with-base",
            action="store_true",
            default=False,
            help="By default base won't be updated. Add parameter to update base",
        )

    def run_command(self):
        super(Update, self).run_command()

        if not self.params.module and not self.params.modules and not self.params.list:
            _logger.error("Update modules list with --list or update module/s with i.e. --module=base or --modules=base,web")
            return

        self.pre_update()
        self.update_modules()

    @with_env
    def pre_update(self):
        if self.params.modules:
            for module in self.params.modules.split(","):
                self.modules_list.append(module)
            self.modules_list = list(set(self.modules_list))

        if self.params.with_depends:
            depends = []
            for module in self.modules_list:
                module_info = load_information_from_description_file(module)
                module_info_depends = module_info.get("depends", [])
                depends = depends + module_info_depends
            self.modules_list = self.modules_list + depends
            self.modules_list = list(set(self.modules_list))

        if "base" in self.modules_list and not self.params.with_base:
            self.modules_list.remove("base")

    def update_modules(self):
        config["reinit"] = "no"        

        if self.modules_list:
            for module in self.modules_list:
                config["update"][module.strip()] = 1
            _logger.info("Update modules: {modules}".format(modules=', '.join(self.modules_list)))
            self.update_database(self.params.database)

    def update_database(self, dbname):
        registry = openerp.modules.registry.RegistryManager.get(dbname, update_module=True)
        updated_modules = self.modules_list
        for updated_module in updated_modules:
            self.post_update_module(updated_module)

    @with_env
    def post_update_module(self, module):
        self.env.cr.autocommit(True)
        package = load_information_from_description_file(module)
        post_update_hook = package.get('post_update_hook')
        if post_update_hook:
            _logger.info("Post Update Hook: {module}".format(module=module))
            py_module = sys.modules['openerp.addons.%s' % (module,)]
            getattr(py_module, post_update_hook)(self.env)


