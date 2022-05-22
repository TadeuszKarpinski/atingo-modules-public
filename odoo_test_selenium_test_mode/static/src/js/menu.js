/** @odoo-module **/
// © 2022 Atingo Tadeusz Karpiński
// License OPL-1 (https://www.odoo.com/documentation/14.0/legal/licenses.html).

import { browser } from "@web/core/browser/browser";
import { routeToUrl } from "@web/core/browser/router_service";
import { registry } from "@web/core/registry";
import { ajax } from "web.ajax";


function odooTestSeleniumTestModeMenu({ env }) {
    // console.log(this);
    // console.log(env);
    // console.log(env.services);
    // console.log(env.orm);
    // console.log(env.orm.rpc);
    // env.services.rpc("ir.config_parameter", "get_odoo_test_selenium_test_mode", [])
    // env["ir.config_parameter"].get_odoo_test_selenium_test_mode()
    // env.services.orm.call({
    //     model: 'ir.config_parameter',
    //     method: 'get_odoo_test_selenium_test_mode',
    //     args: [],
    // }).then(function (param_value) {
    //     alert("a");
    // });
    const param_value = await this.async(() => env.services.orm.call(
        'ir.config_parameter',
        'get_odoo_test_selenium_test_mode',
        [],
    ));
    alert(param_value);
    // var param_value = env.services.orm.call('ir.config_parameter', 'get_odoo_test_selenium_test_mode', []);
    // alert(param_value.resolve());
    // return {
    //     type: "item",
    //     description: env._t("Enter Test Mode"),
    //     callback: () => {
    //         const route = env.services.router.current;
    //         route.search.debug = "";
    //         browser.location.href = browser.location.origin + routeToUrl(route);
    //     },
    //     sequence: 1000,
    // };
}
// function odooTestSeleniumTestModeMenu({ env }) {
//     // console.log(this);
//     // console.log(env);
//     // console.log(env.services);
//     // console.log(env.orm);
//     // console.log(env.orm.rpc);
//     // env.services.rpc("ir.config_parameter", "get_odoo_test_selenium_test_mode", [])
//     // env["ir.config_parameter"].get_odoo_test_selenium_test_mode()
//     // env.services.orm.call({
//     //     model: 'ir.config_parameter',
//     //     method: 'get_odoo_test_selenium_test_mode',
//     //     args: [],
//     // }).then(function (param_value) {
//     //     alert("a");
//     // });
//     var param_value = env.services.orm.call('ir.config_parameter', 'get_odoo_test_selenium_test_mode', []).then(function (param_value) {
//         if (param_value.toLowerCase() !== 'false') {
//             return {
//                 type: "item",
//                 description: env._t("Enter Test Mode"),
//                 callback: () => {
//                     const route = env.services.router.current;
//                     route.search.debug = "";
//                     browser.location.href = browser.location.origin + routeToUrl(route);
//                 },
//                 sequence: 1000,
//             };
//         }
//         if (param_value.toLowerCase() !== 'true') {
//             return {
//                 type: "item",
//                 description: env._t("Leave Test Mode"),
//                 callback: () => {
//                     const route = env.services.router.current;
//                     route.search.debug = "";
//                     browser.location.href = browser.location.origin + routeToUrl(route);
//                 },
//                 sequence: 1010,
//             };
//         }
//     });
// }

registry
    .category("debug")
    .category("default")
    .add("odooTestSeleniumTestModeMenu", odooTestSeleniumTestModeMenu)
