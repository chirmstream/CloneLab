import subprocess
import os
import re


class Repo:
    def __init__(self, url, mirror_url):
        # Assign repo.url, repo.username (project owner), repo.name (project name), and repo.local_dir (where repo is stored locally)
        # Url should include ".git" at the end
        self.url = url

        match = re.search(r"https://(?:www\.)?github.com/(.+)/(.+)\.git", self.url)
        if match:
            self.username = match.group(1)
            if self.username:
                self.name = match.group(2)
        # Need to revise self.local_dir to be set using os library so that windows file paths work
        self.local_dir = "repos" + "/" + self.username + "/" + self.name

    def clone(self):
        # Runs the 'git clone' command and stores repo in repo.local_dir
        subprocess.run(['git', 'clone', self.url, self.local_dir])
        # Saves a copy of the original .git/config file
        self.backup_config()

    def add(self):
        # Runs the 'git commit -a' command to stage all changes
        cwd = os.getcwd()
        os.chdir("repos")
        os.chdir(self.username)
        os.chdir(self.name)
        cwd = os.getcwd()
        subprocess.run(["git", "add", "."], cwd=os.getcwd())

    def commit(self, message):
        # Runs the 'git commit -S -m' command to make a signed commit with message
        # Set cwd back to self.local_dir after fixing __init__
        subprocess.run(["git", "commit", "-S", "-m", message], cwd=os.getcwd())

    def push(self, remote_name, branch_name):
        # Runs the 'git push' command (will push to wherever .git/config file url specifies)
        # Set cwd back to self.local_dir after fixing __init__
        subprocess.run(["git", "push", remote_name, branch_name], cwd=os.getcwd())

    def configure_mirror(self, url, password):
        # Rewrites .git/config url to mirror url.  Sets url with username and password for https pushes.
        self.mirror_url = url
        match = re.search(r"https://(?:www\.)?github.com/(.+)/(.+)\.git", self.mirror_url)
        if match:
            self.mirror_username = match.group(1)
            if self.mirror_username:
                self.mirror_name = match.group(2)
        cwd = os.getcwd()
        os.chdir("repos")
        os.chdir(self.username)
        os.chdir(self.name)
        os.chdir(".git")
        cwd = os.getcwd()
        with open("config", "r") as file:
            old_config = file.read()
        with open("config", "w") as file:
            new_config = re.sub(r"https://(?:www\.)?github.com/(.+)/(.+)\.git", f"https://{self.mirror_username}:{password}@github.com/{self.mirror_username}/{self.mirror_name}.git", old_config)
            file.write(new_config)
        # Reset current working directory
        os.chdir("..")
        os.chdir("..")
        os.chdir("..")
        os.chdir("..")

    def backup_config(self):
        os.chdir("repos")
        os.chdir(self.username)
        os.chdir(self.name)
        os.chdir(".git")
        with open("config", "r") as file:
            config = file.read()
        os.chdir("..")
        os.chdir("..")
        os.chdir("..")
        os.chdir("..")
        cwd = os.getcwd()
        if not os.path.isdir("repo_configs"):
            os.makedirs("repo_configs")
        os.chdir("repo_configs")
        if not os.path.isdir(f"{self.username}"):
            os.makedirs(f"{self.username}")
        os.chdir(f"{self.username}")
        if not os.path.isdir(f"{self.name}"):
            os.makedirs(f"{self.name}")
        os.chdir(f"{self.name}")
        cwd = os.getcwd()
        with open("config", "w") as file:
            file.write(config)
        # Set working directory to CloneLab root folder
        os.chdir("..")
        os.chdir("..")
        os.chdir("..")





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