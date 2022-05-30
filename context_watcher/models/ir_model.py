# -*- coding: utf-8 -*--
# © 2022 Atingo Tadeusz Karpiński
# License OPL-1 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

from lxml import etree
import json
import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)

class IrModel(models.Model):
    _inherit = "ir.model"

    def _patch_with_context(self):
        method_name = "with_context"

        def _wrap_with_context():
            def with_context(self, *args, **kwargs):
                old_ctx = self._context
                self = with_context.origin(self, *args, **kwargs)
                if old_ctx != self._context and self:
                    if getattr(self, "_watch_context", None) and "context_watcher" in self._fields:
                        self._compute_context_field()
                    pass
                return self
            return with_context

        for model in self:
            model_obj = self.env.get(model.model)
            if model_obj is not None:
                model_obj._patch_method(method_name, _wrap_with_context())
                
        return True

    def _register_hook(self):
        models = self.search([])
        models._patch_with_context()
        return super()._register_hook()

    @api.model_create_multi
    def create(self, vals_list):
        ir_models = super().create(vals_list)
        ir_models._patch_with_context()
        return ir_models

    def write(self, vals):
        res = super().write(vals)
        self._patch_with_context()
        return res

        
class ContextBaseAbstract(models.AbstractModel):
    _inherit = "base"

    def _compute_context_field(self):
        for obj in self:
            obj.context_watcher = str(json.dumps(obj._compute_context()))

    def _compute_context(self):
        return self.env.context.copy()

    @api.model
    def _add_magic_fields(self):
        if getattr(self, "_watch_context", None) and "context_watcher" not in self._fields:
                self._add_field("context_watcher", fields.Char(string="Context", automatic=True, compute="_compute_context_field", default="_compute_context_field"))

        return super(ContextBaseAbstract, self)._add_magic_fields()

    @api.model
    def default_get(self, fields_list):
        if getattr(self, "_watch_context", None) and "context_watcher" in self._fields:
            self = self.with_context(self._compute_context())
            
        res = super(ContextBaseAbstract, self).default_get(fields_list)
        return res

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(ContextBaseAbstract, self).fields_view_get(view_id, view_type, toolbar, submenu)

        def create_context_node():
            context_node = etree.XML("<field name='context_watcher'/>")
            context_node.set("invisible", "1")
            context_node.set("modifiers", json.dumps({'invisible': True}))
            return context_node

        if getattr(self, "_watch_context", None) and "context_watcher" in self._fields:
            if view_type == "form":
                doc = etree.XML(res['arch'])
                for node in doc.xpath("//form[1]"):
                    node.insert(0, create_context_node())
                    break
                res['arch'] = etree.tostring(doc, encoding='unicode')

            if view_type == "tree":
                doc = etree.XML(res['arch'])
                for node in doc.xpath("//tree[1]"):
                    context_node = create_context_node()
                    context_node.set("column_invisible", "1")
                    context_node.set("modifiers", json.dumps({'column_invisible': True}))
                    node.insert(0, context_node)
                    break
                res['arch'] = etree.tostring(doc, encoding='unicode')

        return res