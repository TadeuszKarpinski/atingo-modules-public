# -*- coding: utf-8 -*--
# © 2022 Atingo Tadeusz Karpiński
# License OPL-1 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

{
    "name": "Odoo Tests Selenium",
    "version": "9.0.0.1",
    "summary": "Odoo Unit Tests Selenium",
    "author": "Atingo - Tadeusz Karpiński",
    "description": """
    """,
    "category": "Extra Tools",
    "website": "https://www.atingo.pl",
    "depends": [
        "base",
        "odoo_tests",
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
            "selenium",
            "webdriver_manager",
        ],
    },
    # "license": "OPL-1",
}
