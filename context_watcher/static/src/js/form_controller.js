// -*- coding: utf-8 -*--
// © 2022 Atingo Tadeusz Karpiński
// License OPL-1 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

odoo.define("ContextWatcherFormController", function (require) {
    "use strict";

    const WebFormController = require("web.FormController");

    // PART OF SUPER DOMAIN FUNCTIONALITY
    WebFormController.include({
        get_nested_value: function(data, path) {
            var i, len = path.length;
            for (i = 0; typeof data === 'object' && i < len; ++i) {
                data = data[path[i]];
            }
            return data;
        },
        init: function (parent, model, renderer, params) {
            this._super.apply(this, arguments);

            var record = this.model.get(this.handle);
            var modifiers = this.get_nested_value(this, ["renderer", "arch", "attrs", "modifiers"])
            const evaledModifiers = record.evalModifiers(modifiers)

            for (const action_type of ['edit', 'create', 'delete', 'duplicate']) {
                if (evaledModifiers[action_type] != null) {
                    this.activeActions[action_type] = evaledModifiers[action_type];
                }
            }
        },
    })
    return WebFormController
});