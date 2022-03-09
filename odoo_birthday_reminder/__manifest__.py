# -*- coding: utf-8 -*--
# © 2022 Atingo Tadeusz Karpiński
# License AGPL-3.0 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

{
    "name": "Odoo Birthday Reminder",
    "version": "11.0.0.1",
    "summary": "Odoo Birthday Reminder",
    "author": "Atingo - Tadeusz Karpiński",
    "description": """
    """,
    "category": "Extra Tools",
    "website": "https://www.atingo.pl",
    "depends": [
        "base",
        "hr",
    ],
    "data": [
        "data/mail_template_data.xml",
        "data/cron_data.xml",
        "views/hr_department_views.xml",
        "views/hr_employee_views.xml",
    ],
    "images": [
    ],
    "auto_install": False,
    "installable": True,
    "application": False,
    "external_dependencies": {
        "python": [],
    },
    "license": "LGPL-3",
}
