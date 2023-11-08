import subprocess


class Repo:
    # url should include ".git" at the end
    def __init__(self, url):
        self.url = url

    def clone(self, local_dir):
        # Runs the 'git clone' command
        subprocess.run(['git', 'clone', self.url, local_dir])


repo = Repo("https://github.com/chirmstream/VerifiedCommits.git")
repo.clone("repos")