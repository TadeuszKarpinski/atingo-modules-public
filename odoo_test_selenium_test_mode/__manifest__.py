# -*- coding: utf-8 -*--
# © 2022 Atingo Tadeusz Karpiński
# License OPL-1 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

{
    "name": "Odoo Test Selenium Test Mode",
    "version": "15.0.0.1",
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
        # "views/templates.xml",
    ],
    "qweb": [
        # "static/src/xml/template.xml",
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
    'assets': {
        'web.assets_backend': [
            "odoo_test_selenium_test_mode/static/src/css/notification.css",
            "odoo_test_selenium_test_mode/static/src/js/menu.js",
            "odoo_test_selenium_test_mode/static/src/js/test_mode_notification.js",
            "odoo_test_selenium_test_mode/static/src/js/web_bus.js",
        ],
    },
    "license": "OPL-1",
}
