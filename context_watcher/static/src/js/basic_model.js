// -*- coding: utf-8 -*--
// © 2022 Atingo Tadeusz Karpiński
// License OPL-1 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

odoo.define("ContextWatcherBasicModel", function (require) {
    "use strict";

    const WebBasicModel = require("web.BasicModel");
    var Domain = require('web.Domain');

    WebBasicModel.include({
        _evalModifiers: function (element, modifiers) {
            var evaluated = this._super(element, modifiers)
            let evalContext = null;
            for (const k of ['edit', 'create', 'delete', 'duplicate']) {
                const mod = modifiers[k];
                if (mod === undefined || mod === false || mod === true) {
                    if (k in modifiers) {
                        evaluated[k] = !!mod;
                    }
                    continue;
                }
                try {
                    evalContext = evalContext || this._getEvalContext(element);
                    evaluated[k] = new Domain(mod, evalContext).compute(evalContext);
                } catch (e) {
                    throw new Error(_.str.sprintf('for modifier "%s": %s', k, e.message));
                }
            }
            return evaluated;
        },
        async _performOnChange(record, fields, options = {}) {
            var result = await this._super.apply(this, arguments);
            if (result['value'] && result['value']['context_watcher']) {
                record.context = JSON.parse(result.value.context_watcher);
            }
            return result
        },
    })
    return WebBasicModel
});