from optparse import OptionParser
import os

from gitty.git_tools.git_wrapper import GitWrapper
from gitty.git_tools.gitty_ssrs import GittySSRS
from gitty.git_tools.gitty_up import GittyUp


def gitty():
    dir = os.path.split(__file__)[0]
    config_file_path = os.path.join(dir, 'config.json')

    parser = OptionParser()
    parser.add_option("-c", "--number_of_commits", dest="number_of_commits", default=1, help="The number of most recent commits to deploy", metavar="integer")
    parser.add_option("-r", "--repository", dest="repository", default=None, help="Location of the git repo (defaults to the current directory)", metavar="string")
    parser.add_option("-m", "--message", dest="message", default=None, help="The git commit message... defaults to (<username> - Gitty)", metavar="string")
    (options, args) = parser.parse_args()
    action = args[0]

    import win32api
    user = win32api.GetUserName()
    repo_path = options.repository or os.getcwd()
    git_wrapper = GitWrapper(repo_path)
    gitty_up_message = "({0} - GittyUp)".format(user)
    commit_message = " ".join([x for x in [options.message, gitty_up_message] if x])

    if action == 'up':
        g = GittyUp(git_wrapper, user, commit_message)
    elif action == 'ssrs':
        g = GittySSRS(git_wrapper, options.number_of_commits, config_file_path)
    g.execute()


if __name__ == '__main__':
    gitty()
