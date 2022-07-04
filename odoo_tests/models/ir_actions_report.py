# -*- coding: utf-8 -*--
# © 2022 Atingo Tadeusz Karpiński
# License OPL-1 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

import odoo
from odoo import models
import logging
import os

_logger = logging.getLogger(__name__)


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    def download_test_report(self, objects, file_name):
        test_download = odoo.tools.config.get("test_download")

        if test_download:
            (report_data, report_ext) = self._render(objects.ids)
            if report_data:
                download_path = os.path.join(test_download, file_name)
                with open(download_path, "wb") as f:
                    f.write(report_data)
        else:
            _logger.error("Specify --test-download in test parameters !")