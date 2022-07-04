# -*- coding: utf-8 -*--
# © 2022 Atingo Tadeusz Karpiński
# License OPL-1 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

import openerp
from openerp import models
import logging
import os

_logger = logging.getLogger(__name__)


class IrActionsReportXml(models.Model):
    _inherit = "ir.actions.report.xml"

    def download_test_report(self, objects, file_name):
        test_download = openerp.tools.config.get("test_download")

        if test_download:
            (report_data, report_ext) = self.render_report(objects.ids, self.report_name, {})
            if report_data:
                download_path = os.path.join(test_download, file_name)
                with open(download_path, "wb") as f:
                    f.write(report_data)
        else:
            _logger.error("Specify --test-download in test parameters !")