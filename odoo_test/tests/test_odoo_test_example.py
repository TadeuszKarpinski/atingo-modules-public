# -*- coding: utf-8 -*--
# © 2022 Atingo Tadeusz Karpiński
# License OPL-1 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

import mock

from odoo.addons.odoo_test.tests.odoo_test import OdooTestHttpCase

class TestOdooTestExample(OdooTestHttpCase):
    @mock.patch(
        "odoo.http.HttpRequest.validate_csrf",
        return_value=True,
    )
    def test_odoo_test_example_login(self, *args):
        email = "test.odoo.test.example@example.com"
        password = "ASDFGHJK!@#123asdfghjk!@123"
        self.env["res.users"].create(
            {
                "name": "Test Odoo Test Example",
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
        data = dict(csrf_token="asd", login=email, password=password)
        res = self.url_open("/web/login", data=data)

        # self.assertNotIn("/web/login", res.url)
