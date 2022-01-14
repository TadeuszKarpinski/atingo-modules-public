# -*- coding: utf-8 -*--
# © 2021 Atingo Tadeusz Karpiński
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Partner Avatar",
    "version": "14.0.0.4",
    "summary": "Partner Avatar",
    "author": "Tadeusz Karpiński - Atingo",
    "description": """
        Avatar colors can be configured in system parameters: Partner Avatar Colors. First column -> background color, second column -> text color
        Avatar template can be configured in system parameters: Partner Avatar SVG Template.
    """,
    "category": "Partner",
    "website": "https://www.atingo.pl",
    "depends": [
        "base",
    ],
    "data": [
        "data/partner_avatar_data.xml",
    ],
    "images": [
        "static/description/images/thumbnail_screenshot.png", 
        "static/description/images/partner_avatar_scr1.png", 
        "static/description/images/partner_avatar_scr2.png", 
        "static/description/images/partner_avatar_scr3.png", 
        "static/description/images/partner_avatar_scr4.png",
    ],
    "auto_install": False,
    "application": False,
    "installable": True,
    'license': 'LGPL-3',
}
