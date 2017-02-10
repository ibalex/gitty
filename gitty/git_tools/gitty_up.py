from gitty.git_tools.git_wrapper import GitWrapper
from gitty.utils.logging import Logging


class GittyUp:

    def __init__(self, git_wrapper, username, commit_message):
        isinstance(git_wrapper, GitWrapper)
        self.git_wrapper = git_wrapper
        self.username = username
        self.commit_message = commit_message

    def execute(self):
        self.git_wrapper.pull()
        self.git_wrapper.add()
        new_hash = self.git_wrapper.commit(self.commit_message)
        files = self.git_wrapper.get_file_names_from_hash(new_hash)
        results2 = self.git_wrapper.push()
        Logging.log('Git pushed {0} files:\r\n\t\t{1}'.format(len(files), '\r\n\t\t'.join(files)))