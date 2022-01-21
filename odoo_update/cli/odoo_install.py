# -*- coding: utf-8 -*--
# © 2022 Atingo Tadeusz Karpiński
# License AGPL-3.0 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

import logging

import openerp
from openerp.tools.config import config
from .odoo_command import OdooCommand, with_env


_logger = logging.getLogger("Odoo Install")


class Install(OdooCommand):
    """Install Class"""

    def run_command(self):
        super(Install, self).run_command()
        
        if not self.params.module and not self.params.modules and not self.params.list:
            _logger.error("Update modules list with --list or install module/s with i.e. --module=base or --modules=crm,website")
            return

        self.install_modules()

    @with_env
    def install_modules(self):
        config["reinit"] = "no"        

        if self.modules_list:
            module_obj = self.env["ir.module.module"]
            for module in self.modules_list:
                module_id = module_obj.search([("name", "=", module), ('state', 'in', ['to install', 'uninstalled'])])
                if module_id:
                    _logger.info("Install modules: {modules}".format(modules=', '.join(self.modules_list)))
                    module_id.button_immediate_install()

            openerp.modules.registry.RegistryManager.get(self.params.database, update_module=True)

