from suds.transport.https import WindowsHttpAuthenticated  # @UnresolvedImport
import suds  # @UnresolvedImport
from gitty.ssrs.ssrs_report_upload_record import SSRSReportUploadedRecord
from gitty.utils.logging import Logging


class SSRSReportService2005Wrapper(object):

    def __init__(self, url, server_nice_name, username, password):
        self.url = url
        self.server_nice_name = server_nice_name
        transport = WindowsHttpAuthenticated(username=str(username), password=str(password))
        self.client = suds.client.Client(url=url, transport=transport)
        self._upload_history = []

    def upload(self, file_name, folder_path, overwrite, content_bytes):
        warnings = None
        try:
            warnings = self.client.service.CreateReport(file_name, folder_path, overwrite, content_bytes, None)
            if warnings:
                Logging.log_to_file(SSRSReportUploadedRecord(folder_path, file_name, warnings))
        except Exception as e:
            print(SSRSReportUploadedRecord(folder_path, file_name, warnings, e))
