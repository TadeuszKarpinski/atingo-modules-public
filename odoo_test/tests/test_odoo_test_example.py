# -*- coding: utf-8 -*--
# © 2022 Atingo Tadeusz Karpiński
# License OPL-1 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

import mock
from odoo.tests.common import HttpCase
from odoo.tests.common import TransactionCase


class TestOdooTestExample(HttpCase):
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

        for resp_hist in res.history:
            self.assertNotIn("/web?debug", resp_hist.url)

class TestOdooTestExampleTransactionCase(TransactionCase):

    def test_odoo_test_example_transaction_case(self):
        group = self.env["res.groups"].create({"name": "Test Group"})
        self.assertEqual(group.name, "Test Group")