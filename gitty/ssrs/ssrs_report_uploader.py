import argparse
import base64
import sys
import os

from gitty.ssrs.ssrs_report_service_wrapper import SSRSReportService2005Wrapper
from gitty.utils.file_path_helper import FilePathHelper
from gitty.utils.logging import Logging


class SSRSReportUploader(object):

    def __init__(self, local_reports_dir, ssrs_soap_wrapper, accepted_file_extensions=[".rdl", ".png"]):
        self._ssrs_soap_wrapper_list = []
        self._local_reports_root_dir = local_reports_dir
        self._accepted_file_extensions = accepted_file_extensions
        self._ssrs_soap_wrapper = ssrs_soap_wrapper
        self.url = ssrs_soap_wrapper.url
        isinstance(self._ssrs_soap_wrapper, SSRSReportService2005Wrapper)

    def upload_single(self, file_path):
        if not self._is_valid_file(file_path):
            return
        ssrs_server_rel_path = self._get_ssrs_rel_path(file_path)
        file_name = FilePathHelper.get_file_name_without_extension(file_path)
        Logging.log("Uploading '{0}' to '{1}' folder".format(file_name, ssrs_server_rel_path))
        content_bytes = self._get_file_contents(file_path)
        self._ssrs_soap_wrapper.upload(file_name, ssrs_server_rel_path, True, content_bytes)

    def _get_ssrs_rel_path(self, file_path):
        rel_local_dir_path = FilePathHelper.get_relative_directory_path(self._local_reports_root_dir, file_path)
        server_rel_path = FilePathHelper.convert_windows_path_to_unix(rel_local_dir_path)
        return server_rel_path

    def _get_file_contents(self, file_path):
        with open(file_path, 'r') as f:
            content_bytes = f.read()
        return base64.encodestring(content_bytes)

    def _is_valid_file(self, file_path):
        if not FilePathHelper.is_valid_file_path(file_path):
            Logging.log("Skipping (can't find)'{0}'".format(file_path))
            return False
        if not FilePathHelper.is_valid_file_ext(file_path, self._accepted_file_extensions):
            Logging.log("Skipping (file type) '{0}'".format(file_path))
            return False
        return True


def set_args(f):
    local_file_path = os.path.join("C:\\git\\pe_ssrs_templates\\Prod Reports\\", f)
    sys.argv.append('-file')
    sys.argv.append(local_file_path)


if __name__ == "__main__":
    # set_args(r"Capital Roll Forward\Capital Roll Forward - With ROR.rdl"")
    # set_args(r"Investor Capital\Investor Capital Statement (TRPT).rdl")
    set_args(r"Investor Capital\Investor Capital Statement (GBRK).rdl")

    parser = argparse.ArgumentParser(prog=sys.argv, description='Upload an SSRS template to all servers at once!')
    parser.add_argument('-file', type=str, required=True, help='''Local rdl file path (example: 'C:\\ssrs\\reports\\Ending Valuations.rdl') ''')
    args = parser.parse_args()
    rdl_file_path = args.file

    dev_url = "http://hse-nj-dba-01:8000/ReportServer_DB01/ReportService2005.asmx"
    uat_url = "http://hst-ny-srpt-01/ReportServer/ReportService2005.asmx"
    prod_url = "http://hss-py-ssrs-01/ReportServer/ReportService2005.asmx"

    uploader = SSRSReportUploader("C:\\git\\pe_ssrs_templates\\", SSRSReportService2005Wrapper(dev_url, "DEV", "fds\service-pedi", ""))
    uploader.upload_single(rdl_file_path)
