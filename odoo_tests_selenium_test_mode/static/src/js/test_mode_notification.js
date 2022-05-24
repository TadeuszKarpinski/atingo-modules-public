// © 2022 Atingo Tadeusz Karpiński
// License OPL-1 (https://www.odoo.com/documentation/12.0/legal/licenses.html).

odoo.define("odoo_tests_selenium_test_mode.notification", function (require) {
    "use strict";

    var Model = require('web.Model');
    var core = require("web.core");

    var odoo_tests_selenium_test_mode_notification_bar = $('<div class="odoo-test-selenium-test-mode-notification">⚠️⚠️⚠️ You are in test mode ! All changes will be ROLLBACKED ! ⚠️⚠️⚠️</div>');
    odoo_tests_selenium_test_mode_notification_bar.hide();

    function show_odoo_tests_selenium_test_mode_notification_bar() {
        var model = new Model('ir.config_parameter');
        model.call('get_odoo_tests_selenium_test_mode').then(function (param_value) {
            if (param_value.toLowerCase() === 'true') {
                odoo_tests_selenium_test_mode_notification_bar.show();
            } else {
                odoo_tests_selenium_test_mode_notification_bar.hide();
            }
        });
    }

    core.bus.on("web_client_ready", null, function () {
        $("body").prepend(odoo_tests_selenium_test_mode_notification_bar);
        show_odoo_tests_selenium_test_mode_notification_bar();
    });

    core.bus.on("odoo_tests_selenium_enter_test_mode", null, function () {
        setTimeout(function () {
            show_odoo_tests_selenium_test_mode_notification_bar();
        }, 6000);
    });

    core.bus.on("odoo_tests_selenium_leave_test_mode", null, function () {
        setTimeout(function () {
            show_odoo_tests_selenium_test_mode_notification_bar();
        }, 6000);
    });
});
