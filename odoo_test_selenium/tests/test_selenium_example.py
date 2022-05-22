# -*- coding: utf-8 -*--
# © 2022 Atingo Tadeusz Karpiński
# License OPL-1 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

from odoo.addons.odoo_test_selenium.tests.odoo_test_selenium import SeleniumHttpCase


class TestSeleniumExample(SeleniumHttpCase):
    
    def test_selenium_example_login(self):
        email = "test.odoo.test.selenium.example@example.com"
        password = "ASDFGHJK!@#123asdfghjk!@123"
        self.env["res.users"].create(
            {
                "name": "Test Selenium Example",
                "login": email,
                "password": password,
                "groups_id": [
                    (
                        6,
                        0,
                        [
                            self.env.ref("base.group_user").id,
                            self.env.ref("base.group_no_one").id,
                        ],
                    )
                ],
            }
        )
        self.sbrowser_url_open("/web")

        # first use wrong credentials
        self.sbrowser.find_element_by_name("login").send_keys("wrong.email@example.com")
        self.sbrowser.find_element_by_name("password").send_keys(
            "wrong.password", self.KEYS.RETURN
        )
        self.assertIn("/web/login", self.sbrowser.current_url)

        # login with good credentials
        self.sbrowser.find_element_by_name("login").clear()
        self.sbrowser.find_element_by_name("password").clear()
        self.sbrowser.find_element_by_name("login").send_keys(email)
        self.sbrowser.find_element_by_name("password").send_keys(
            password, self.KEYS.RETURN
        )

        self.assertNotIn("/web/login", self.sbrowser.current_url)
        self.assertIn("/web", self.sbrowser.current_url)

        self.sleep()  # for example purposes test never will be closed
