# -*- coding: utf-8 -*--
# © 2022 Atingo Tadeusz Karpiński
# License OPL-1 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

import logging
import re

from odoo.exceptions import ValidationError
from odoo import models, _, api

_logger = logging.getLogger(__name__)

class View(models.Model):
    _inherit = 'ir.ui.view'

    @api.model
    def postprocess_and_fields(self, model, node, view_id):
        def check_node(model, node, view_id):
            for key, val in node.items():
                if key == 'attrs' and "context.get" in val:
                    model_obj = self.env[model]
                    view = self.browse(view_id)

                    if not getattr(model_obj, "_watch_context", False):
                        view_name = ('%s (%s)' % (view.name, view.xml_id)) if view.xml_id else view.name
                        raise ValidationError(_(
                            'Invalid view {0} definition in {1}. Add _watch_context = True in {2} model declaration to use context.get'.format(
                                view_name, view.arch_fs, view.model,
                            )
                        ))

                    context_gets = re.findall(r'context\.get\((.*?)\)', val)
                    for context_get in context_gets:
                        node.set('attrs', val.replace(f'context.get({context_get})', str(f'"context.get({context_get})"')))

            for child in node:
                check_node(model, child, view_id)

        check_node(model, node, view_id)
        res = super(View, self).postprocess_and_fields(model, node, view_id)
        return res
        