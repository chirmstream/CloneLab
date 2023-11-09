import subprocess
import os
import re
import sys
import shutil



class Repo:
    def __init__(self, url, mirror_url):
        # Assign repo.url, repo.username (project owner), repo.name (project name), and repo.local_dir (where repo is stored locally)
        # Url should include ".git" at the end
        self.url = url
        self.mirror_url = mirror_url
        self.set_dirs()

    def set_dirs(self):
        match = re.search(r"https://(?:www\.)?github.com/(.+)/(.+)\.git", self.url)
        if match:
            self.username = match.group(1)
            if self.username:
                self.name = match.group(2)
        # Set repo local path
        if not os.path.isdir("repos"):
            os.makedirs("repos")
        os.chdir("repos")
        if not os.path.isdir(f"{self.username}"):
            os.makedirs(f"{self.username}")
        os.chdir(f"{self.username}")
        if not os.path.isdir(f"{self.name}"):
            os.makedirs(f"{self.name}")
        os.chdir(f"{self.name}")
        self.dir = os.getcwd()
        # Reset current working directory
        os.chdir("..")
        os.chdir("..")
        os.chdir("..")
        match = re.search(r"https://(?:www\.)?github.com/(.+)/(.+)\.git", self.mirror_url)
        if match:
            self.mirror_username = match.group(1)
            if self.mirror_username:
                self.mirror_name = match.group(2)
        # Set mirror repo local path
        if not os.path.isdir("mirror_repos"):
            os.makedirs("mirror_repos")
        os.chdir("mirror_repos")
        if not os.path.isdir(f"{self.mirror_username}"):
            os.makedirs(f"{self.mirror_username}")
        os.chdir(f"{self.mirror_username}")
        if not os.path.isdir(f"{self.mirror_name}"):
            os.makedirs(f"{self.mirror_name}")
        os.chdir(f"{self.mirror_name}")
        self.mirror_dir = os.getcwd()
        # Reset current working directory
        os.chdir("..")
        os.chdir("..")
        os.chdir("..")

    def clone(self):
        # Runs the 'git clone' command for both original and mirror repo
        subprocess.run(['git', 'clone', self.url, self.dir])
        subprocess.run(['git', 'clone', self.mirror_url, self.mirror_dir])

    def sync(self):
        # Rsyncs original repo to mirror repo (excluding .git/) and then
        src = self.dir + "/"
        dest = self.mirror_dir + "/"
        subprocess.run(["rsync", "-rvh", "--progress", "--exclude", ".git/", src, dest])

    def add(self):
        # Runs the 'git commit -a' command to stage all changes on mirror repo
        os.chdir("mirror_repos")
        os.chdir(self.mirror_username)
        os.chdir(self.mirror_name)
        subprocess.run(["git", "add", "."], cwd=os.getcwd())
        os.chdir("..")
        os.chdir("..")
        os.chdir("..")

    def commit(self, message):
        # Runs the 'git commit -S -m' command to make a signed commit with message
        # Set cwd back to self.local_dir after fixing __init__
        subprocess.run(["git", "commit", "-S", "-m", message], cwd=self.mirror_dir)

    def push(self, remote_name, branch_name):
        # Runs the 'git push' command (will push to wherever .git/config file url specifies)
        # Set cwd back to self.local_dir after fixing __init__
        subprocess.run(["git", "push", remote_name, branch_name], cwd=os.getcwd())

    def mirror_auth(self, password):
        # Rewrites mirror_repo .git/config url to to include username & password for https pushes.
        os.chdir("mirror_repos")
        os.chdir(self.mirror_username)
        os.chdir(self.mirror_name)
        os.chdir(".git")
        try:
            with open("config", "r") as file:
                old_config = file.read()
        except FileNotFoundError:
            sys.exit("error, mirror_repo not found")
        with open("config", "w") as file:
            new_config = re.sub(r"https://(?:www\.)?github.com/(.+)/(.+)\.git", f"https://{self.mirror_username}:{password}@github.com/{self.mirror_username}/{self.mirror_name}.git", old_config)
            file.write(new_config)
        # Reset current working directory
        os.chdir("..")
        os.chdir("..")
        os.chdir("..")
        os.chdir("..")

    # Getter for url
    @property
    def url(self):
        return self._url

    # Setter for url
    @url.setter
    def url(self, url):
        # Add url validation via regex here
        self._url = url

    # Getter for mirror_url
    @property
    def mirror_url(self):
        return self._mirror_url

    # Setter for mirror_url
    @mirror_url.setter
    def mirror_url(self, mirror_url):
        # Add url validation via regex here
        self._mirror_url = mirror_url

    # Getter for username
    @property
    def username(self):
        return self._username

    # Setter for username
    @username.setter
    def username(self, username):
        self._username = username

    # Getter for name
    @property
    def name(self):
        return self._name

    # Setter for name
    @name.setter
    def name(self, name):
        self._name = name

    # Getter for dir
    @property
    def dir(self):
        return self._dir
    
    # Setter for dir
    @dir.setter
    def dir(self, dir):
        self._dir = dir

    # Getter for mirror_username
    @property
    def mirror_username(self):
        return self._mirror_username

    # Setter for mirror_username
    @mirror_username.setter
    def mirror_username(self, mirror_username):
        self._mirror_username = mirror_username

    # Getter for mirror_name
    @property
    def mirror_name(self):
        return self._mirror_name

    # Setter for mirror_name
    @mirror_name.setter
    def mirror_name(self, mirror_name):
        self._mirror_name = mirror_name

    # Getter for mirror_dir
    @property
    def mirror_dir(self):
        return self._mirror_dir

    # Setter for mirror_dir
    @mirror_dir.setter
    def mirror_dir(self, mirror_dir):
        self._mirror_dir = mirror_dir


#original_url = "https://github.com/dhouck/anti-creeper-grief.git"
#mirror_url = "https://github.com/chirmstream/CloneLab-Testing.git"

#repo = Repo(original_url, mirror_url)

#repo.sync()



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