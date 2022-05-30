![Banner](static/description/images/banner.png?raw=true "Banner")

Context Watcher
------------------------------
With this module developer can use context.get in view domains and pass context from models to views.

Examples:

In this dummy example name field of partner will be hidden when the name is "Hide Me! In general with this module developer can remove all dummy computed fields.

partner.py
```
from odoo import models, api

class Partner(models.Model):
    _inherit = "res.partner"
    <b>_watch_context = True</b>

    def _compute_context(self):
        res = super(Partner, self)._compute_context()
        if self.name == "Hide Me!":
            res["hide_name"] = True
        return res

    @api.onchange("name")
    def onchange_name(self):
        for partner in self:
            if partner.name == "Hide Me!":
                partner.with_context(hide_name=True)
            else:
                partner.with_context(hide_name=False)
```
Notes: User must add _watch_context = True. Function _compute_context() is always evaluated for one record.

partner_views.xml
```
<record id="res_partner_view_form_inherit_context_watcher" model="ir.ui.view">
	<field name="name">res.partner.view.form.inherit.context.watcher</field>
	<field name="model">res.partner</field>
	<field name="inherit_id" ref="base.view_partner_form"/>
	<field name="arch" type="xml">
		<xpath expr="//field[@name='name']" position="attributes">
			<attribute name="attrs">{"invisible": [(context.get('hide_name'), '=', True)]}</attribute>
		</xpath>
	</field>
</record>
```

[Check out my youtube channel to learn more!](https://www.youtube.com/channel/UCf5TCwpMFTfA7g76Pk7SxwA)

In case of any questions don't hesitate to email me: tadeusz.karpinski@gmail.com
