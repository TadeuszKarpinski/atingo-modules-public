// © 2022 Atingo Tadeusz Karpiński
// License OPL-1 (https://www.odoo.com/documentation/13.0/legal/licenses.html).

odoo.define('odoo_tests_selenium_test_mode.TestModeMenu', function (require) {
    "use strict";

    var DebugManager = require('web.DebugManager');
    var ajax = require('web.ajax');

    var TestModeMenu = DebugManager.include({
        start: function () {
            this._super.apply(this, arguments);

            var self = this;
            this._rpc({
                model: 'ir.config_parameter',
                method: 'get_odoo_tests_selenium_test_mode',
                args: [],
            }).then(function (param_value) {
                self.odoo_tests_selenium_test_mode = (param_value.toLowerCase() === 'true');
            });
            return this;
        },
        enter_test_mode: function () {
            var self = this;
            self._rpc({
                model: 'ir.config_parameter',
                method: 'get_odoo_tests_selenium_test_mode',
                args: [],
            }).then(function (param_value) {
                if (param_value.toLowerCase() !== 'false') {
                    alert("You are already in TEST MODE !");
                    location.reload();
                } else {
                    var session = self.getSession();
                    session.rpc("/odoo_tests_mode_notification", { "channel": "odoo_tests_selenium_test_mode", "message": "enter_test_mode" }).then(function () {
                        setTimeout(function () {
                            ajax.post('/enter_test_mode', {});
                            location.reload();
                        }, 3000);
                    });
                }
            });
        },
        leave_test_mode: function () {
            var self = this;
            this._rpc({
                model: 'ir.config_parameter',
                method: 'get_odoo_tests_selenium_test_mode',
                args: [],
            }).then(function (param_value) {
                if (param_value.toLowerCase() !== 'true') {
                    alert("You aren't in TEST MODE !");
                    location.reload();
                } else {
                    var session = self.getSession();
                    ajax.post('/leave_test_mode', {});

                    setTimeout(function () {
                        session.rpc("/odoo_tests_mode_notification", { "channel": "odoo_tests_selenium_test_mode", "message": "leave_test_mode" }).then(function () {
                            location.reload();
                        });
                    }, 3000);
                }
            });
        },
    });
    return TestModeMenu;
});
