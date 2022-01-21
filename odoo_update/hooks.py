# -*- coding: utf-8 -*--
# © 2022 Atingo Tadeusz Karpiński
# License AGPL-3.0 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

import logging

_logger = logging.getLogger(__name__)

def post_update_hook(env):
    _logger.info("Post Update Hook Example")