// © 2022 Atingo Tadeusz Karpiński
// License OPL-1 (https://www.odoo.com/documentation/13.0/legal/licenses.html).

odoo.define("OdooTestsSeleniumTestModeWebBus", function (require) {
    "use strict";

    var WebClient = require("web.WebClient");
    var core = require("web.core");

    require("bus.BusService");

    WebClient.include({
        show_application: function () {
            var res = this._super();
            this.odoo_tests_selenium_test_mode_start_polling();
            return res;
        },
        odoo_tests_selenium_test_mode_start_polling: function () {
            this.odoo_tests_selenium_test_mode = "odoo_tests_selenium_test_mode";
            this.odoo_tests_selenium_test_mode_all_channels = [
                this.odoo_tests_selenium_test_mode,
            ];
            this.call("bus_service", "startPolling");
            this.call("bus_service", "addChannel", this.odoo_tests_selenium_test_mode);
            this.call("bus_service", "on", "notification", this, this.odoo_tests_selenium_test_mode_notification);
        },
        odoo_tests_selenium_test_mode_notification: function (notifications) {
            var self = this;
            _.each(notifications, function (notification) {
                var channel = notification[0];
                var message = notification[1];
                if (
                    self.odoo_tests_selenium_test_mode_all_channels !== null &&
                    self.odoo_tests_selenium_test_mode_all_channels.indexOf(channel) > -1
                ) {
                    self.odoo_tests_selenium_test_mode_web_bus_on_message(channel, message);
                }
            });
        },
        odoo_tests_selenium_test_mode_web_bus_on_message: function (channel, message) {
            if (channel == this.odoo_tests_selenium_test_mode) {
                if (message == "leave_test_mode") {
                    core.bus.trigger('odoo_tests_selenium_leave_test_mode');
                }
                if (message == "enter_test_mode") {
                    core.bus.trigger('odoo_tests_selenium_enter_test_mode');
                }
            }
            return true;
        },
    });
});