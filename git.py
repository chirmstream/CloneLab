import subprocess
import os
import re
import sys
from shutil import rmtree


class Repo:
    def __init__(self, url, mirror_url):
        # Assign repo.url, repo.username (project owner), repo.name (project name), and repo.local_dir (where repo is stored locally)
        # Url should include ".git" at the end
        self.url = url
        self.mirror_url = mirror_url
        self.set_dirs()
        self.get(self.url, self.dir)
        self.get(self.mirror_url, self.mirror_dir)
        print(f"Starting mirroring for {self.url}")

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

    def get(self, git_url, local_path):
        if len(os.listdir(local_path)) == 0:
            try:
                subprocess.run(['git', 'clone', git_url, local_path])
            except:
                self.get_private(git_url, local_path, self.mirror_username, self.mirror_password)
        else:
            rmtree(f"{local_path}")
            self.set_dirs()
            try:
                subprocess.run(['git', 'clone', git_url, local_path])
            except:
                self.get_private(git_url, local_path, self.mirror_username, self.mirror_password)
        self.reset_directory()

    def get_private(self, git_url, local_path, username, password):
        git_url = f"https://{username}:{password}@{self.mirror_domain}/{username}/{self.mirror_name}.git"
        if len(os.listdir(local_path)) == 0:
            subprocess.run(['git', 'clone', git_url, local_path])
        else:
            rmtree(f"{local_path}")
            self.set_dirs()
            subprocess.run(['git', 'clone', git_url, local_path])

    def get_commits(self, repository_folder):
        # Some code borrowed from https://gist.github.com/091b765a071d1558464371042db3b959.git, thank you simonw
        os.chdir(f"{repository_folder}")
        log_raw = subprocess.check_output(["git", "log", "--reverse"], stderr=subprocess.STDOUT).decode("utf-8", errors='ignore').split("\n")
        commits = self.process_log(log_raw)
        return commits

    def process_log(self, log):
        commits = []
        current_commit = {
            "commit":"",
            "author":"",
            "date":"",
            "message":""
        }
        for _ in range(len(log)):
            line = log[_]
            if line[:7] == "commit ":
                commit = line[7:]
                current_commit["commit"] = commit
            elif line[:8] == "Author: ":
                author = line[8:]
                current_commit["author"] = author
            elif line[:6] == "Date: ":
                date = line[8:]
                current_commit["date"] = date
            else:
                try:
                    if log[_ + 1][:7] != "commit ":
                        message = current_commit["message"] + line[4:]
                        current_commit["message"] = message
                    else:
                        message = current_commit["message"] + line
                        current_commit["message"] = message
                        next_commit = current_commit.copy()
                        commits.append(next_commit)
                        current_commit["message"] = ""
                except:
                    message = current_commit["message"] + line
                    current_commit["message"] = self.add_newline(message)
                    next_commit = current_commit.copy()
                    commits.append(next_commit)
        return commits

    def add_newline(self, s):
        s = s + "\n"
        return s

    def next(self, commits, mirror_commits):
        # Can assume last correct commit is commit # 1 zero indexed
        for _ in range(1, len(commits)):
            try:
                commit = commits[_]
                mirror_commit = mirror_commits[_]
            except:
                return _
            if self.commits_match(commit, mirror_commit) == False:
                return _
        sys.exit("Commits already mirrored")

    def sync(self):
        commits = self.get_commits(self.dir)
        mirror_commits = self.get_commits(self.mirror_dir)
        self.sync_first_commit(commits[0], mirror_commits[0])
        print(f"Mirroring remaining commits...")
        n = self.next(commits, mirror_commits)
        # Create temp branch for mirror repo
        if n == 1:
            os.chdir(f"{self.mirror_dir}")
            subprocess.run(["git", "checkout", "-b", "temp"])
        else:
            os.chdir(f"{self.mirror_dir}")
            subprocess.run(["git", "checkout", "-b", "temp", mirror_commits[n - 1]['commit']])
        commits_made = 0
        for _ in range(n, len(commits)):
            if commits_made > 150:
                self.update()
                # After pushing new commits we need reset back to how it was before we pushed code
                os.chdir(f"{self.mirror_dir}")
                rmtree(f"{self.mirror_dir}")
                self.set_dirs()
                self.get(self.mirror_url, self.mirror_dir)
                mirror_commits = self.get_commits(self.mirror_dir)
                subprocess.run(["git", "checkout", "-b", "temp", mirror_commits[_ - 1]['commit']])
                commits_made = 0
            os.chdir(f"{self.dir}")
            subprocess.run(["git", "checkout", commits[_]['commit']])
            self.rsync()
            os.chdir(f"{self.mirror_dir}")
            self.add()
            message = self.create_commit_msg(commits[_])
            self.commit(message)
            commits_made = commits_made + 1
        self.update()
        print(f"Successfully mirrored {self.url} to {self.mirror_url}")

    def create_commit_msg(self, commit):
        pull_requst = re.search(r"^e: ([a-zA-Z0-9]+)* ([a-zA-Z0-9]+)Merge pull request #([0-9]+) from ([a-zA-Z0-9-_]+)/([a-zA-Z0-9-_]+)(.*)$", commit["message"])
        if pull_requst:
            matches = pull_requst.groups()
            n = len(matches)
            parents = []
            for _ in range(0, n - 4):
                parents.append(matches[_])
            branch_parents = ""
            for parent in parents:
                branch_parents = branch_parents + f" {parent}"
            pull_request_num = matches[n - 4]
            branch_author = matches[n - 3]
            branch_repo = matches[n - 2]
            merge_msg = matches[n - 1]
            message = (
                f"Merge pull request #{pull_request_num} from {branch_author}/{branch_repo}\n"
                f"{merge_msg}\n"
                f"Branch Parents:{branch_parents}\n\n"
                f"Original Commit Hash: {commit['commit']}\n"
                f"Original Author: {commit['author']}\n"
                f"Original Date: {commit['date']}\n"
                f"Repository {self.url} cloned using CloneLab"
            )
            return message
        branch_merge = re.search(r"^e: ([a-zA-Z0-9]+)* ([a-zA-Z0-9]+)Merge branch ([a-zA-Z0-9/']+) of ([a-z]+://[a-zA-Z/\.]+)(.)*$", commit["message"])
        if branch_merge:
            matches = branch_merge.groups()
            n = len(matches)
            parents = []
            for _ in range(0, n - 3):
                parents.append(matches[_])
            branch_parents = ""
            for parent in parents:
                branch_parents = branch_parents + f" {parent}"
            branch_name = matches[n - 3]
            branch_repo = matches[n - 2]
            if matches[n - 1] == None:
                message = (
                    f"Merge branch {branch_name} of {branch_repo}\n"
                    f"Branch Parents:{branch_parents}\n\n"
                    f"Original Commit Hash: {commit['commit']}\n"
                    f"Original Author: {commit['author']}\n"
                    f"Original Date: {commit['date']}\n"
                    f"Repository {self.url} cloned using CloneLab"
                )
                return message
            else:
                merge_msg = matches[n - 1]
                message = (
                    f"Merge branch {branch_name} of {branch_repo}\n"
                    f"{merge_msg}\n"
                    f"Branch Parents:{branch_parents}\n\n"
                    f"Original Commit Hash: {commit['commit']}\n"
                    f"Original Author: {commit['author']}\n"
                    f"Original Date: {commit['date']}\n"
                    f"Repository {self.url} cloned using CloneLab"
                )
                return message
        message = (
            f"{commit['message']}\n"
            f"Original Commit Hash: {commit['commit']}\n"
            f"Original Author: {commit['author']}\n"
            f"Original Date: {commit['date']}\n"
            f"Repository {self.url} cloned using CloneLab"
        )
        return message

    def sync_first_commit(self, first_commit, first_mirror_commit):
        print(f"Checking first commit...")
        if self.commits_match(first_commit, first_mirror_commit) == False:
            print(f"Syncing first commit...")
            first_commit_hash = first_commit['commit']
            os.chdir(f"{self.dir}")
            subprocess.run(["git", "checkout", first_commit_hash])
            os.chdir(f"{self.mirror_dir}")
            # Create orphan branch 'temp', and delete everthing
            subprocess.run(["git", "switch", "--orphan", "temp"])
            subprocess.run(["git", "rm", "-rf", "."])
            subprocess.run(["git", "clean", "-fd"])
            self.rsync()
            self.add()
            message = self.create_commit_msg(first_commit)
            self.commit(message)
            # Push code to remote branch 'temp' and delete 'temp' afterwards
            os.chdir(f"{self.mirror_dir}")
            subprocess.run(["git", "push", "-u", "origin", "temp"])
            subprocess.run(["git", "push", "-f", "origin", "temp:main"])
            subprocess.run(["git", "switch", "main"])
            subprocess.run(["git", "branch", "--delete", "temp"])
            subprocess.run(["git", "push", "origin", "--delete", "temp"])
            # Delete both repos and reclone from remote
            self.get(self.url, self.dir)
            self.get(self.mirror_url, self.mirror_dir)
        else:
            print(f"First commit already already mirrored...")

    def commits_match(self, current_commit, mirror_commit):
        commit_hash = current_commit["commit"]
        if commit_hash in mirror_commit["message"]:
                return True
        return False

    def rsync(self):
        # remove mirror repository files, then rsync original repository files to mirror
        os.chdir(f"{self.mirror_dir}")
        subprocess.run(["git", "rm", "-rf", "."])
        src = self.dir + "/"
        dest = self.mirror_dir + "/"
        #subprocess.run(["rsync", "-rvh", "--progress", "--exclude", ".git/", src, dest])
        subprocess.run(["rsync", "-a", "--exclude", ".git/", src, dest])

    def update(self):
            # Pushes temp branch, copies temp branch to main, then deletes temp branch
            os.chdir(f"{self.mirror_dir}")
            subprocess.run(["git", "push", "-u", "origin", "temp"])
            subprocess.run(["git", "push", "-f", "origin", "temp:main"])
            subprocess.run(["git", "switch", "main"])
            subprocess.run(["git", "branch", "--delete", "temp"])
            subprocess.run(["git", "push", "origin", "--delete", "temp"])
            os.chdir(f"{self.dir}")
            subprocess.run(["git", "switch", "-"])

    def add(self):
        subprocess.run(["git", "add", "."], cwd=self.mirror_dir)
        self.reset_directory()

    def get_empty_directories(self, path):
        # Credit for this function goes to tutorialspoint.com, it was a very simple function though so I felt okay copying it.
        # https://www.tutorialspoint.com/get-the-list-of-all-empty-directories-in-python#:~:text=By%20checking%20if%20both%20the,directory%20and%20not%20a%20file.
        empty_dirs = []
        for entry in os.scandir(path):
            if entry.is_dir() and not any(entry.is_file() for entry in os.scandir(entry.path)):
                empty_dirs.append(entry.path)
        return empty_dirs

    def commit(self, message):
        # Check for empty folders
        empty_directories = self.get_empty_directories(self.mirror_dir)
        if empty_directories:
            for empty_directory in empty_directories:
                os.chdir(f"{empty_directory}")
                with open(".gitkeep", "w") as file:
                    file.write("")
            print(empty_directories)
        subprocess.run(["git", "commit", "--allow-empty", "-S", "-m", message], cwd=self.mirror_dir)

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
