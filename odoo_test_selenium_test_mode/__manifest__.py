# -*- coding: utf-8 -*--
# © 2022 Atingo Tadeusz Karpiński
# License OPL-1 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

{
    "name": "Odoo Test Selenium Test Mode",
    "version": "12.0.0.1",
    "summary": "Odoo Unit Tests Selenium Test Mode",
    "author": "Atingo - Tadeusz Karpiński",
    "description": """
    """,
    "category": "Extra Tools",
    "website": "https://www.atingo.pl",
    "depends": [
        "base",
    ],
    "data": [
        "data/data.xml",
        "views/templates.xml",
    ],
    "qweb": [
        "static/src/xml/template.xml",
    ],
    "images": [
        "static/description/images/banner.png",
    ],
    "auto_install": False,
    "installable": True,
    "application": False,
    "external_dependencies": {
        "python": [],
    },
    "license": "OPL-1",
}
