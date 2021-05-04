# -*- coding: utf-8 -*-

{
    "name": "Partner Avatar",
    "version": "14.0.0.3",
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
    "images": ["static/desciption/images/partner_avatar_scr1.png", "static/desciption/images/partner_avatar_scr2.png", "static/desciption/images/partner_avatar_scr3.png", "static/desciption/images/partner_avatar_scr4.png"],
    "auto_install": False,
    "application": False,
    "installable": True,
}
