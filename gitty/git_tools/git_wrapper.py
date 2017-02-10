from git.repo.base import Repo
import os

from gitty.utils.file_path_helper import FilePathHelper
from gitty.utils.logging import Logging


class GitWrapperRepositoryInitializationError(Exception): pass


class GitWrapper(object):

    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.repo = self._init_repo()
        self.git = self.repo.git
        self.origin = self._get_origin()

    def _init_repo(self):
        return Repo(self.repo_path)

    def _is_local_repo(self):
        return os.path.exists(self.repo_path) and ".git" in os.listdir(self.dir_path)

    def _clone(self):
        return Repo.clone_from(self.url, self.dir_path, depth=10)

    def _get_origin(self):
        if not self.repo or not self.repo.remotes:
            return None
        remotes = [r for r in self.repo.remotes if r.name == 'origin']
        return remotes[0] if remotes else None

    def get_latest_local_hash(self):
        self.git.execute("git rev-parse master") # assumes branch is 'master'

    def get_latest_remote_hash(self):
        self.fetch()
        self.git.execute("git rev-parse origin") # assumes remote is 'origin'

    def pull(self):
        try:
            results = self.origin.pull()
        except Exception as e:
            Logging.log('\r\n\tGITTY UP PULL FAILED: Resolve any conflicts between your pending commit and the remote repository and try again.\r\n')
            raise e
        return results

    def add(self):
        return self.repo.git.add(update=True)

    def commit(self, message):
        return self.repo.index.commit(message)

    def push(self):
        return self.origin.push()

    def get_changed_files(self, number_of_commits=1):
        self.origin.fetch()
        hashes = self._get_last_n_revision_hashes(number_of_commits)
        file_names = []
        for h in hashes:
            file_names.extend(self.get_file_names_from_hash(h))
        return list(set(file_names))

    def _get_last_n_revision_hashes(self, n):
        hashes = self.git.execute("git log -n {0} --pretty=format:\"%h\"".format(n))
        return [h for h in hashes.split('\n') if h.strip(' ')]

    def get_file_names_from_hash(self, rev_hash):
        files = self.git.execute("git diff-tree --no-commit-id --name-only -r {0}".format(rev_hash))
        f1 = lambda path: "{0}/{1}".format(self.repo_path, path)
        f2 = FilePathHelper.convert_file_path_to_environment_standard
        return [f2(f1(n)) for n in files.split('\n') if n.strip(' ')]


if __name__ == "__main__":
    # dir_path = r"C:\temp\test"
    dir_path = r"C:\git\test"
    w = GitWrapper(dir_path)
    # results = w.diff()
    w.add()
    w.get_have_files_changed()
    # results = w.get_changed_files(8)
    # print(str(results))
    print("\r\n\r\n\t\tDONE...")
