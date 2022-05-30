# -*- coding: utf-8 -*--
# © 2022 Atingo Tadeusz Karpiński
# License OPL-1 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

import logging
import re

from odoo.exceptions import ValidationError
from odoo import models, _

_logger = logging.getLogger(__name__)

class View(models.Model):
    _inherit = 'ir.ui.view'

    def _validate_attrs(self, node, name_manager, node_info):
        res = super(View, self)._validate_attrs(node, name_manager, node_info)
        model_obj = self.env["ir.model"]
        for view in self:
            for field, use in name_manager.mandatory_fields.copy().items():
                if "context.get" in field:
                    model = self.env[view.model]
                    if not getattr(model, "_watch_context", False):
                        view_name = ('%s (%s)' % (view.name, view.xml_id)) if view.xml_id else view.name
                        raise ValidationError(_(
                            'Invalid view %(name)s definition in %(file)s. Add _watch_context = True in %(model)s model declaration to use context.get',
                            name=view_name, file=view.arch_fs, model=view.model,
                        ))
                    del name_manager.mandatory_fields[field]

        return res

    def postprocess(self, node, current_node_path, editable, name_manager):
        attrs = node.get('attrs')
        if attrs:
            context_gets = re.findall(r'context\.get\((.*?)\)', attrs)
            for context_get in context_gets:
                node.set('attrs', attrs.replace(f'context.get({context_get})', str(f'"context.get({context_get})"')))
        return super(View, self).postprocess(node, current_node_path, editable, name_manager)
