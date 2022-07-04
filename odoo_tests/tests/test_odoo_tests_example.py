# -*- coding: utf-8 -*--
# © 2022 Atingo Tadeusz Karpiński
# License OPL-1 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

from openerp.addons.odoo_tests.tests.odoo_tests import OdooTestsHttpCase
from openerp.tests.common import TransactionCase

class TestOdooTestsExample(OdooTestsHttpCase):

    def test_odoo_tests_example_login(self, *args):
        email = "test.odoo.test.example@example.com"
        password = "ASDFGHJK!@#123asdfghjk!@123"
        self.env["res.users"].create(
            {
                "name": "Test Odoo Tests Example",
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

class TestOdooTestsExampleTransactionCase(TransactionCase):

    def test_odoo_tests_example_transaction_case(self):
        group = self.env["res.groups"].create({"name": "Test Group"})
        self.assertEqual(group.name, "Test Group")

    def test_odoo_tests_example_report_download(self):
        """e.g. --test-download=/home/odoo/odoo-atingo
        """
        report = self.env.ref("base.report_ir_model_overview")
        model = self.env["ir.model"].search([("model", "=", "base")])
        report.download_test_report(model, "model_report.pdf")
