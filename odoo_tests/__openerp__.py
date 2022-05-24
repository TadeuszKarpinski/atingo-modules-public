# -*- coding: utf-8 -*--
# © 2022 Atingo Tadeusz Karpiński
# License OPL-1 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

{
    "name": "Odoo Tests",
    "version": "9.0.0.1",
    "summary": "Odoo Unit Tests",
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
        "python": [
            "unittest2",
        ],
    },
    # "license": "OPL-1",
}
