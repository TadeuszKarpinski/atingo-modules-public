# -*- coding: utf-8 -*--
# © 2021 Atingo Tadeusz Karpiński
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import ast
import base64
import logging
import random
import re

from xml.sax.saxutils import escape as xml_escape

from odoo import api, models, _

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.constrains("name")
    def constrains_name(self):
        for partner in self:
            vals = partner.get_new_avatar({"name": partner.name})
            vals.pop("name")
            partner.write(vals)

    def create(self, vals):
        if vals:
            if type(vals) is list:
                vals = vals[0]
            vals.pop("image_1920", None)
            vals = self.get_new_avatar(vals)
        partners = super().create(vals)
        return partners

    def get_new_avatar(self, vals):
        name = vals.get("name", False)
        image_1920 = vals.get("image_1920", False)
        is_generated = False
        is_empty = False

        current_image = self.image_1920
        if current_image:
            try:
                current_image_decoded = base64.b64decode(current_image).decode("utf-8")
                is_generated = 'data-partner-avatar="true"' in current_image_decoded
            except:
                pass
        else:
            is_empty = True

        if name and not image_1920 and (is_generated or is_empty):
            vals["image_1920"] = self.get_png_avatar(name)
        return vals

    def set_new_avatar(self):
        for partner in self:
            partner.write(partner.get_new_avatar({"name": partner.name}))
        return True

    def get_png_avatar(self, name):
        COLORS = ast.literal_eval(
            self.env.ref("partner_avatar.partner_avatar_colors").value.strip()
        )
        INITIALS_SVG_TEMPLATE = self.env.ref(
            "partner_avatar.partner_avatar_svg_template"
        ).value.strip()
        INITIALS_SVG_TEMPLATE = re.sub("(\s+|\n)", " ", INITIALS_SVG_TEMPLATE)

        initials = ":)"

        name = name.strip()
        if name:
            split_name = name.split(" ")
            if len(split_name) > 1:
                initials = split_name[0][0] + split_name[-1][0]
            else:
                initials = split_name[0][0]

        random_color = random.choice(COLORS)
        svg_avatar = INITIALS_SVG_TEMPLATE.format(
            **{
                "bg_color": random_color[0],
                "text_color": random_color[1],
                "text": xml_escape(initials.upper()),
            }
        ).replace("\n", "")

        encoded_avatar = base64.b64encode(svg_avatar.encode())
        return encoded_avatar