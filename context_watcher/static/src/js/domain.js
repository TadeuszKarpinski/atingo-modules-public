// -*- coding: utf-8 -*--
// © 2022 Atingo Tadeusz Karpiński
// License OPL-1 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

odoo.define("ContextWatcherDomain", function (require) {
    "use strict";

    const WebDomain = require("web.Domain");

    WebDomain.include({
        compute: function (values) {
            if (_.isArray(this._data)) {
                var fieldName = this._data[0];
                if (fieldName.includes('context.get')) {
                    fieldName = fieldName.replace("context.get", "context_get");
                    this._data[0] = fieldName;
                } 
                if (fieldName.includes('context_get')) {
                    var context = JSON.parse(values["context_watcher"]);
                    function context_get(key, default_value=false) {
                        return context[key] || default_value;
                    }
                    values[fieldName] = eval(fieldName);
                }
            }
            return this._super.apply(this, arguments);
        },
    })
    return WebDomain;
});