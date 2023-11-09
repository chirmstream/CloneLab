import subprocess
import os
import re


class Repo:
    # url should include ".git" at the end
    def __init__(self, url):
        self.url = url
        self.cloned = False
        match = re.search(r"https://(?:www\.)?github.com/(.+)/(.+)\.git", self.url)
        if match:
            self.username = match.group(1)
            if self.username:
                self.name = match.group(2)

        self.local_dir = "repos" + "/" + self.username + "/" + self.name

    def clone(self):
        # Runs the 'git clone' command
        subprocess.run(['git', 'clone', self.url, self.local_dir])
        self.cloned = True

    def add(self):
        # Runs the 'git commit -a' command to stage all changes
        subprocess.run(["git", "add", "."], cwd=self.local_dir)

    def commit(self, message):
        # Runs the 'git commit -S -m' command
        subprocess.run(["git", "commit", "-S", "-m", message], cwd=self.local_dir)

    def push(self, remote_name, branch_name):
        # Runs the 'git push' command
        subprocess.run(["git", "push", remote_name, branch_name], cwd=self.local_dir)

    def configure(self, password):
        # Load current .git/config
        cwd = os.getcwd()
        os.chdir("repos")
        os.chdir(self.username)
        os.chdir(self.name)
        os.chdir(".git")
        cwd = os.getcwd()
        with open("config", "r") as file:
            old_config = file.read()
        with open("config", "w") as file:
            new_config = re.sub(r"https://(?:www\.)?github.com/(.+)/(.+)\.git", f"https://{self.username}:{password}@github.com/{self.username}/{self.name}.git", old_config)
            file.write(new_config)


token_password = "token"
repo = Repo("https://github.com/chirmstream/CloneLab-Testing.git")

#repo.clone()
#repo.configure(token_password)

repo.add()
repo.commit("test commit message")
repo.push("origin", "main")




# Regular expression examples
def validate(ip):
    numerical = re.search(r"^[\d]{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip)
    if numerical:
        ip = ip.split(".")
        for num in ip:
            if int(num) > 255:
                return False
        return True
    return False


def parse(s):
    embeded_video = re.search(
        r"\"(https?://(?:www\.)?youtube.com/embed/[a-zA-Z].+)\"", s
    )
    if embeded_video:
        embeded_video = embeded_video.group(1)
        url = re.sub(
            r"https?://(?:www\.)?youtube.com/embed/", "https://youtu.be/", embeded_video
        )
        return url
    return None