# -*- coding: utf-8 -*--
# © 2022 Atingo Tadeusz Karpiński
# License AGPL-3.0 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

{
    "name": "Odoo Update",
    "version": "15.0.0.1",
    "summary": "Odoo Update/Install/Uninstall Modules",
    "author": "Atingo - Tadeusz Karpiński",
    "description": """
    """,
    "category": "Extra Tools",
    "website": "https://www.atingo.pl",
    "depends": [
        "base",
    ],
    "data": [],
    "images": [
        "static/description/images/banner.png",
    ],
    "auto_install": True,
    "installable": True,
    "application": False,
    "external_dependencies": {
        "python": [],
    },
    "post_update_hook": "post_update_hook",
    "license": "LGPL-3",
}
