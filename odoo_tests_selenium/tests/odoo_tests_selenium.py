# -*- coding: utf-8 -*--
# © 2022 Atingo Tadeusz Karpiński
# License OPL-1 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

import logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager

from odoo.tests.common import HOST
import odoo
import time

from odoo.addons.odoo_tests.tests.odoo_tests import OdooTestsHttpCase

browsers = []
_logger = logging.getLogger(__name__)


def create_browser(ctx):
    chrome_options = ChromeOptions()

    browser_visible = ctx.get("browser_visible", False)
    selenium_params = ctx.get("selenium_params", [])

    if not browser_visible and not selenium_params:
        options = ["--headless", "--disable-gpu"]
        for option in options:
            chrome_options.add_argument(option)

    for selenium_param in selenium_params:
        chrome_options.add_argument(selenium_param)

    browser = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    browsers.append(browser)
    return browser


class SeleniumHttpCase(OdooTestsHttpCase):
    def __init__(self, *args, **kwargs):
        self.sbrowser_domain = "http://%s:%s" % (HOST, odoo.tools.config.get("http_port", "8069"))
        self.KEYS = Keys
        super(SeleniumHttpCase, self).__init__(*args, **kwargs)

    @property
    def sbrowser(self):
        if not browsers:
            raise Exception(
                "Add parameter --with-browser to run browser without GUI, or use --with-browser-visible to run browser with GUI"
            )
        return browsers[0]

    def sleep(self, seconds=1000):
        time.sleep(seconds)

    def tearDown(self):
        super(SeleniumHttpCase, self).tearDown()
        self.sbrowser_cleanup()

    def sbrowser_cleanup(self):
        self.sbrowser_url_open("/web/session/logout")
        self.sbrowser.delete_all_cookies()
        self.sbrowser_url_open("about:blank")

    def sbrowser_url_open(self, url):
        if url.startswith("/"):
            url = self.sbrowser_domain + url
        self.sbrowser.get(url)
        self.sleep(1)

    def authenticate(self, user, password):
        res = super(SeleniumHttpCase, self).authenticate(user, password)
        if self.sbrowser:
            cookies = self.opener.cookies.get_dict()
            if cookies:
                self.sbrowser_url_open(self.sbrowser_domain)
                for cookie_name, cookie_value in cookies.items():
                    self.sbrowser.add_cookie(
                        {"name": cookie_name, "value": cookie_value}
                    )
        return res
