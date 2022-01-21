# -*- coding: utf-8 -*--
# © 2022 Atingo Tadeusz Karpiński
# License AGPL-3.0 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

import logging

import odoo
from odoo.tools.config import config
from .odoo_command import OdooCommand 


_logger = logging.getLogger("Odoo Install")


class Install(OdooCommand):
    """Install Class"""

    def run_command(self):
        super(Install, self).run_command()
        
        if not self.params.module and not self.params.modules and not self.params.list:
            _logger.error(f"Update modules list with --list or install module/s with i.e. --module=base or --modules=crm,website")
            return

        self.install_modules()

    def install_modules(self):
        config["reinit"] = "no"        

        if self.modules_list:
            for module in self.modules_list:
                config["init"][module.strip()] = 1
            _logger.info(f"Install modules: {', '.join(self.modules_list)}")
            odoo.modules.registry.Registry.new(self.params.database, update_module=True)

