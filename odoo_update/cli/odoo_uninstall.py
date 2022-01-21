# -*- coding: utf-8 -*--
# © 2022 Atingo Tadeusz Karpiński
# License AGPL-3.0 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

import logging

from .odoo_command import OdooCommand, with_env 


_logger = logging.getLogger("Odoo Uninstall")


class Uninstall(OdooCommand):
    """Uninstall Class"""

    def __init__(self):
        super(Uninstall, self).__init__()

        self.parser.add_argument(
            "--force",
            dest="force",
            default=False,
            action="store_true",
            help="Force uninstallation",
        )

    def run_command(self):
        super(Uninstall, self).run_command()
        
        if not self.params.module and not self.params.modules and not self.params.list:
            _logger.error("Update modules list with --list or uninstall module/s with i.e. --module=base or --modules=crm,website")
            return

        self.uninstall_modules()

    @with_env
    def uninstall_modules(self):
        if self.modules_list:
            module_obj = self.env["ir.module.module"]
            for module in self.modules_list:
                module_id = module_obj.search([("name", "=", module), ('state', 'in', ['installed', 'to upgrade', 'to install'])])
                if module_id:
                    modules = module_id.downstream_dependencies(module_id)
                    if not self.params.force:
                        i = raw_input("Modules to uninstall: {modules}. Uninstall? [y/N]".format(modules=', '.join(modules.mapped('name'))))
                        if i.lower() != "y":
                            continue
                    modules.button_immediate_uninstall()

