from datetime import datetime


class SSRSReportUploadedRecord(object):

    def __init__(self, server_path, rdl_file_name, warnings, exception=None):
        self.server_path = server_path
        self.rdl_file_name = rdl_file_name
        self.warnings = warnings
        self.exception = exception
        self.timestamp = datetime.utcnow()

    def get_dict_repr(self):
        return {"Server Path": self.server_path,
                "Rdl File": self.rdl_file_name,
                "Status": ("Y" if not self.exception else "N"),
                "Timestamp": str(self.timestamp),
                "Warnings": self.warnings,
                "Exception": self.exception.message if self.exception else None}

    def __str__(self):
        d = self.get_dict_repr()
        result = '\n'
        result += '\nTimestamp: {0}'.format(d['Timestamp'])
        result += '\nRdl File: {0}'.format(d['Rdl File'])
        result += '\nServer Path: {0}'.format(d['Server Path'])
        result += '\nStatus: {0}'.format(d['Status'])
        result += '\nException: {0}'.format(d['Exception'])
        result += '\nWarnings: {0}\n'.format(d['Warnings'])
        return result
