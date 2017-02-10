import json
import sys
import os

from gitty.ssrs.ssrs_report_service_wrapper import SSRSReportService2005Wrapper
from gitty.ssrs.ssrs_report_uploader import SSRSReportUploader
from gitty.utils.user_input import get_username_and_password
from gitty.utils.file_path_helper import FilePathHelper
from gitty.git_tools.git_wrapper import GitWrapper
from gitty.utils.logging import Logging


class GittySSRS:

    def __init__(self, git_wrapper, number_of_commits, config_file_path=None):
        config_dir = os.path.split(sys.modules[__name__].__file__)[0]
        self.config_path = config_file_path or "{0}/config.json".format(config_dir)
        isinstance(git_wrapper, GitWrapper)
        self.git_wrapper = git_wrapper
        self.number_of_commits = number_of_commits

    def execute(self):
        server_details = self._read_config().get('ssrs_servers', [])
        uploaders = [self._configure_uploader(d) for d in server_details]
        if not uploaders:
            Logging.log('There appears to be no ssrs servers listed in the config.json file')
            return
        files = self._parse_revisions(self.number_of_commits)
        if not files:
            Logging.log("There appears to be no files changed in the last {0} commits...".format(self.number_of_commits))
            return
        files = [self._normalize_file_name(f) for f in files]
        for uploader in uploaders:
            self._deploy_to_ssrs(files, uploader)

    def _read_config(self):
        if not os.path.exists(self.config_path):
            raise EnvironmentError('Config file ({0}) missing'.format(self.config_path))
        return json.loads(open(self.config_path, 'r').read())

    def _configure_uploader(self, server_details):
        url = str(server_details['ssrs_service']).strip()
        try:
            name = str(server_details['name']).strip()
            user = str("{0}\{1}".format(str(server_details['domain']).strip(), server_details['username'])).strip()
            pw = str(server_details['password']).strip()
            if not user or not pw:
                user, pw = get_username_and_password("SSRS credentials required ({0})".format(name))
                domain = str(server_details['domain']).strip()
                user = '{0}\\{1}'.format(domain, user)
            ssrs_wrapper = SSRSReportService2005Wrapper(url, name, user, pw)
            ssrs_root_dir = "{0}{1}".format(self.git_wrapper.repo_path, server_details.get('root_dir', ''))
            ssrs_root_dir = FilePathHelper.convert_file_path_to_environment_standard(ssrs_root_dir.replace('//', '/'))
            return SSRSReportUploader(ssrs_root_dir, ssrs_wrapper)
        except Exception as e:
            Logging.log('Error configuring uploader for ssrs server ({0})'.format(url))
            raise e

    def _parse_revisions(self, number_of_commits=1):
        try:
            files = self.git_wrapper.get_changed_files(number_of_commits)
            return list(set(files)) if files else []
        except Exception as e:
            Logging.log("git error finding changed files using git wrapper")
            raise e

    def _normalize_file_name(self, file_name):
        file_path = file_name
        file_path = FilePathHelper.convert_file_path_to_environment_standard(file_path)
        file_path = FilePathHelper.convert_to_absolute_path(file_path)
        file_path = FilePathHelper.convert_file_path_to_environment_standard(file_path)
        if not FilePathHelper.is_valid_file_path(file_path):
            raise IOError('File does not exist ({0})'.format(file_path))
        return file_path

    def _deploy_to_ssrs(self, file_paths, uploader):
        try:
            Logging.log("\r\n")
            Logging.log("SSRS SOAP Service: {0}".format(uploader.url))
            isinstance(uploader, SSRSReportUploader)
            for f in file_paths:
                uploader.upload_single(f)
            Logging.log('Finished...')
        except:
            print("error deploying to ssrs ({0})".format(uploader.url))

