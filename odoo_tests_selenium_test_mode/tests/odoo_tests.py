# -*- coding: utf-8 -*--
# © 2022 Atingo Tadeusz Karpiński
# License OPL-1 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

import requests

import odoo
from odoo.tests.common import HttpCase, get_db_name


class OdooTestsHttpCase(HttpCase):
    def setUp(self):
        super(HttpCase, self).setUp()

        if self.registry_test_mode:
            self.registry.enter_test_mode(self.cr)
            self.addCleanup(self.registry.leave_test_mode)
        # setup a magic session_id that will be rollbacked
        self.session = odoo.http.root.session_store.new()
        self.session_id = self.session.sid
        self.session.db = get_db_name()
        odoo.http.root.session_store.save(self.session)
        # setup an url opener helper
        self.opener = requests.Session()
        self.opener.cookies["session_id"] = self.session_id
