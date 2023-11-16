import subprocess
import os
import re
import sys


class Repo:
    def __init__(self, url, mirror_url):
        # Assign repo.url, repo.username (project owner), repo.name (project name), and repo.local_dir (where repo is stored locally)
        # Url should include ".git" at the end
        self.url = url
        self.mirror_url = mirror_url
        self.set_dirs()

    def set_dirs(self):
        # Setup repo domains, usernames, and project names
        self.domain, self.username, self.name = self.parse_url(self.url)
        self.mirror_domain, self.mirror_username, self.mirror_name = self.parse_url(self.mirror_url)
        # Setup repo folder structure
        self.reset_directory()
        # Set repo local path
        if not os.path.isdir("repos"):
            os.makedirs("repos")
        os.chdir("repos")
        if not os.path.isdir(self.username):
            os.makedirs(self.username)
        os.chdir(self.username)
        if not os.path.isdir(self.name):
            os.makedirs(self.name)
        os.chdir(self.name)
        self.dir = os.getcwd()
        self.reset_directory()
        # setup mirrored repo folder structure
        if not os.path.isdir("mirror_repos"):
            os.makedirs("mirror_repos", exist_ok=True)
        os.chdir("mirror_repos")
        if not os.path.isdir(self.mirror_username):
            os.makedirs(self.mirror_username)
        os.chdir(f"{self.mirror_username}")
        if not os.path.isdir(self.mirror_name):
            os.makedirs(self.mirror_name)
        os.chdir(self.mirror_name)
        self.mirror_dir = os.getcwd()
        self.reset_directory()

    def get(self):
        print(f"Starting mirroring for {self.url}")
        # Runs the 'git clone' command for original repo
        if len(os.listdir(self.dir)) == 0:
            subprocess.run(['git', 'clone', self.url, self.dir])
        else:
            os.chdir(self.dir)
            subprocess.run(['git', 'pull'])
        # Runs the 'git clone' command for mirror repo
        if len(os.listdir(self.mirror_dir)) == 0:
            try: 
                subprocess.run(['git', 'clone', self.mirror_url, self.mirror_dir])
            except:
                print("repository appears to be private, trying login")
                url = f"https://{self.mirror_username}:{password}@{self.mirror_domain}/{self.mirror_username}/{self.mirror_name}.git"
                subprocess.run(['git', 'clone', url, self.mirror_dir])
        else:
            os.chdir(self.mirror_dir)
            subprocess.run(['git', 'pull'])
        self.reset_directory()

    def get_commits(self):
        # Some code borrowed from https://gist.github.com/091b765a071d1558464371042db3b959.git, thank you simonw
        os.chdir(f"{self.dir}")
        log_raw = subprocess.check_output(["git", "log", "--reverse"], stderr=subprocess.STDOUT).decode("utf-8").split("\n")
        commits = self.process_log(log_raw)
        os.chdir(f"{self.mirror_dir}")
        mirror_log_raw = subprocess.check_output(["git", "log", "--reverse"], stderr=subprocess.STDOUT).decode("utf-8").split("\n")
        mirror_commits = self.process_log(mirror_log_raw)
        return commits, mirror_commits

    def process_log(self, log):
        commits = []
        current_commit = {
            "commit":"",
            "author":"",
            "date":"",
            "message":""
        }
        for _ in range(len(log)):
            if log[_][:7] == "commit ":
                commit = log[_][7:]
                current_commit["commit"] = commit
            elif log[_][:8] == "Author: ":
                author = log[_][8:]
                current_commit["author"] = author
            elif log[_][:6] == "Date: ":
                date = log[_][8:]
                current_commit["date"] = date
            else:
                try:
                    if log[_ + 1][:7] != "commit ":
                        message = current_commit["message"] + log[_]
                        current_commit["message"] = self.add_newline(message)
                    else:
                        message = current_commit["message"] + log[_]
                        current_commit["message"] = self.add_newline(message)
                        commits.append(current_commit)
                        current_commit["message"] = ""
                except:
                    message = current_commit["message"] + log[_]
                    current_commit["message"] = self.add_newline(message)
                    commits.append(current_commit)
        return commits

    def add_newline(self, s):
        s = s + "\n"
        return s

    def sync(self):
        commits, mirror_commits = self.get_commits()
        # Process mirror_commits, cross reference messages (which contain information regarding original commit \
        # hashes, authors, and messages.)
        # Go back in time until they match (if they do at all.)
        # Starting with the first commit that does not match, checkout said commit on original repo,
        # rsync original repo commit to mirror
        # add/commit (with message indicating what commit it is copying), and push to remote
        # Repeat until synced

        # Rsyncs original repo to mirror repo (excluding .git/) and then
        src = self.dir + "/"
        dest = self.mirror_dir + "/"
        subprocess.run(["rsync", "-rvh", "--progress", "--exclude", ".git/", src, dest])

    def add(self):
        # Runs the 'git commit -a' command to stage all changes on mirror repo
        subprocess.run(["git", "add", "."], cwd=self.mirror_dir)
        self.reset_directory()

    def commit(self, message):
        # Runs the 'git commit -S -m' command to make a signed commit with message
        subprocess.run(["git", "commit", "-S", "-m", message], cwd=self.mirror_dir)

    def push(self, remote_name="", branch_name=""):
        # Runs the 'git push' command (will push to wherever .git/config file url specifies)
        subprocess.run(["git", "push"], cwd=self.mirror_dir)

    def set_mirror_login(self, password):
        # Rewrites mirror_repo .git/config url to to include username & password for https pushes.
        os.chdir("mirror_repos")
        os.chdir(self.mirror_username)
        os.chdir(self.mirror_name)
        if not os.path.isdir(".git"):
            sys.exit("missing mirror git config file, please initialize repository with a readme")
        os.chdir(".git")
        try:
            with open("config", "r") as file:
                old_config = file.read()
        except FileNotFoundError:
            sys.exit("error, mirror_repo not found")
        with open("config", "w") as file:
            new_config = re.sub(r"https://(?:www\.)?(.+)/(.+)/(.+)\.git", f"https://{self.mirror_username}:{password}@{self.mirror_domain}/{self.mirror_username}/{self.mirror_name}.git", old_config)
            file.write(new_config)
        self.reset_directory()

    def parse_url(self, url):
        try:
            match = re.search(r"https://(?:www\.)?(.+)/(.+)/(.+)\.git", url)
            if match:
                domain = match.group(1)
                if domain:
                    username = match.group(2)
                    if username:
                        name = match.group(3)
        except:
            sys.exit(f"Error, invalid url: {url}")
        return (domain, username, name)

    def reset_directory(self):
        os.chdir(os.path.expanduser("~"))
        if not os.path.isdir("CloneLab-data"):
            os.makedirs("CloneLab-data")
        os.chdir("CloneLab-data")

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
