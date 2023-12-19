import subprocess
import os
import re
import sys
from shutil import rmtree


class Repo:
    def __init__(self, url, kind):
        self.url = url
        self.kind = kind
        if self.url[:4] == "git@":
            self.authentication = "ssh"
        else:
            self.authentication = "https"
        self.username, self.password, self.domain, self.repo_owner, self.repo_name = self.parse_url(self.url)
        self.path = self.get_path(self.kind, self.repo_owner, self.repo_name)

    def get_path(self, kind, repo_owner, repo_name):
        if kind == "original":
            path = os.path.join(os.path.expanduser("~"), "CloneLab-data", "repos", repo_owner, repo_name)
        elif kind == "mirror":
            path = os.path.join(os.path.expanduser("~"), "CloneLab-data", "mirror_repos", repo_owner, repo_name)
        return path

    def clone(self, original_repository):
        # Clone repositories
        self.get(original_repository)
        self.get(self)
        # Process commit history for both repositories
        commits = self.get_commits(original_repository)
        mirror_commits = self.get_commits(self)
        # Clone original repo to mirror repo
        self.sync_first_commit(original_repository, commits[0], mirror_commits[0])
        # Find next commit to mirror
        n = self.next(commits, mirror_commits)
        if n == 1:
            os.chdir(f"{self.path}")
            subprocess.run(["git", "checkout", "-b", "temp"])
        else:
            os.chdir(f"{self.path}")
            subprocess.run(["git", "checkout", "-b", "temp", mirror_commits[n - 1]['commit']])
        # Sync remaining commits
        commits_made = 0
        for _ in range(n, len(commits)):
            if commits_made > 15:
                self.update()
                os.chdir(f"{original_repository.path}")
                subprocess.run(["git", "switch", "-"])
                # After pushing new commits we need reset back to how it was before we pushed code
                self.get(original_repository)
                self.get(self)
                mirror_commits = self.get_commits(self)
                subprocess.run(["git", "checkout", "-b", "temp", mirror_commits[_ - 1]['commit']])
                commits_made = 0
            os.chdir(f"{original_repository.path}")
            subprocess.run(["git", "checkout", commits[_]['commit']])
            self.rsync(original_repository.path, self.path)
            os.chdir(f"{self.path}")
            self.add()
            message = self.create_commit_msg(commits[_])
            self.commit(message)
            commits_made = commits_made + 1
        self.update()
        os.chdir(f"{original_repository.dir}")
        subprocess.run(["git", "switch", "-"])
        print(f"Successfully mirrored {original_repository.url} to {self.url}")

    def get(self, repository):
        if os.path.exists(repository.path):
            pass
        else:
            os.makedirs(repository.path)
        if len(os.listdir(repository.path)) == 0:
                subprocess.run(['git', 'clone', repository.url, repository.path])
        else:
            rmtree(f"{repository.path}")
            subprocess.run(['git', 'clone', repository.url, repository.path])

    def get_commits(self, repository):
        # Some code borrowed from https://gist.github.com/091b765a071d1558464371042db3b959.git, thank you simonw
        path = repository.path
        os.chdir(f"{path}") #Error here.
        try:
            log_raw = subprocess.check_output(["git", "log", "--reverse"], stderr=subprocess.STDOUT).decode("utf-8", errors='ignore').split("\n")
            commits = self.process_log(log_raw)
            return commits
        except:
            sys.exit(f"Error parsing commits for {repository.url}")

    def process_log(self, log):
        commits = []
        current_commit = {
            "commit":"",
            "author":"",
            "date":"",
            "message":""
        }
        message = None
        for _ in range(len(log)):
            line = log[_]
            if message == None:
                commit = re.search(r"^commit ([a-zA-Z0-9]+)$", line)
                if commit:
                    current_commit["commit"] = commit.group(1)
                    continue
                author = re.search(r"^Author: (.+) <(.+)>$", line)
                if author:
                    current_commit["author"] = f"{author.group(1)} <{author.group(2)}>"
                    continue
                date = re.search(r"^Date:[ ]+(.+)$", line)
                if date:
                    current_commit["date"] = date.group(1)
                    continue
                if line == "":
                    message = ""
            else:
                message = message + line.strip()
                if line == "":
                    current_commit["message"] = message
                    message = None
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

    def create_commit_msg(self, commit):
        # github seems to have changed message from starting with e: to or: name <email>...
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
                f"Original author: {commit['author']}\n"
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
                    f"Original author: {commit['author']}\n"
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
                    f"Original author: {commit['author']}\n"
                    f"Original Date: {commit['date']}\n"
                    f"Repository {self.url} cloned using CloneLab"
                )
                return message
        message = (
            f"{commit['message']}\n"
            f"Original Commit Hash: {commit['commit']}\n"
            f"Original author: {commit['author']}\n"
            f"Original Date: {commit['date']}\n"
            f"Repository {self.url} cloned using CloneLab"
        )
        return message

    def sync_first_commit(self, original_repository, first_commit, first_mirror_commit):
        print(f"Checking first commit...")
        if self.commits_match(first_commit, first_mirror_commit) == False:
            print(f"Syncing first commit...")
            first_commit_hash = first_commit['commit']
            os.chdir(f"{original_repository.path}")
            subprocess.run(["git", "checkout", first_commit_hash])
            # Create orphan branch 'temp', and delete everthing
            os.chdir(f"{self.path}")
            subprocess.run(["git", "switch", "--orphan", "temp"])
            self.rsync(original_repository.path, self.path)
            self.add()
            message = self.create_commit_msg(first_commit)
            self.commit(message)
            # Push code to remote branch 'temp' and delete 'temp' afterwards
            os.chdir(f"{self.path}")
            subprocess.run(["git", "push", "-u", "origin", "temp"])
            subprocess.run(["git", "push", "-f", "origin", "temp:main"])
            subprocess.run(["git", "switch", "main"])
            subprocess.run(["git", "branch", "--delete", "temp"])
            subprocess.run(["git", "push", "origin", "--delete", "temp"])
            # Delete both repos and reclone from remote
            self.get(original_repository)
            self.get(self)
        else:
            print(f"First commit already already mirrored...")

    def commits_match(self, current_commit, mirror_commit):
        commit_hash = current_commit["commit"]
        if commit_hash in mirror_commit["message"]:
                return True
        return False

    def rsync(self, source, destination):
        # remove mirror repository files, then rsync original repository files to mirror
        os.chdir(destination)
        src = source + "/"
        dest = destination + "/"
        subprocess.run(["rsync", "-a", "--exclude", ".git/", src, dest])

    def update(self):
            # Pushes temp branch, copies temp branch to main, then deletes temp branch
            os.chdir(f"{self.path}")
            subprocess.run(["git", "push", "-u", "origin", "temp"])
            subprocess.run(["git", "push", "-f", "origin", "temp:main"])
            subprocess.run(["git", "switch", "main"])
            subprocess.run(["git", "branch", "--delete", "temp"])
            subprocess.run(["git", "push", "origin", "--delete", "temp"])

    def add(self):
        subprocess.run(["git", "add", "."], cwd=self.path)

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
        empty_directories = self.get_empty_directories(self.path)
        if empty_directories:
            for empty_directory in empty_directories:
                os.chdir(f"{empty_directory}")
                with open(".gitkeep", "w") as file:
                    file.write("")
            print(empty_directories)
        subprocess.run(["git", "commit", "--allow-empty", "-S", "-m", message], cwd=self.path)

    def push(self, remote_name="", branch_name=""):
        # Runs the 'git push' command (will push to wherever .git/config file url specifies)
        subprocess.run(["git", "push"], cwd=self.mirror_dir)

    def parse_url(self, url):
        # Match authenticated https repos
        match = re.search(r"^https://(.+):(.+)@(.+)/(.+)/(.+).git$", url)
        if match:
            username = match.group(1)
            password = match.group(2)
            domain = match.group(3)
            repo_owner = match.group(4)
            repo_name = match.group(5)
            return username, password, domain, repo_owner, repo_name
        # Match non-authenticated https repos
        match = re.search(r"^https://(.+)/(.+)/(.+).git$", url)
        if match:
            username = None
            password = None
            domain = match.group(1)
            repo_owner = match.group(2)
            repo_name = match.group(3)
            return username, password, domain, repo_owner, repo_name
        # Match ssh authenticated repos
        match = re.search(r"^git@(.+):(.+)/(.+).git$", url)
        if match:
            username = None
            password = None
            domain = match.group(1)
            repo_owner = match.group(2)
            repo_name = match.group(3)
            return username, password, domain, repo_owner, repo_name
        # No valid url found
        sys.exit(f"Error, invalid url: {url}")

    def reset_directory(self):
        os.chdir(os.path.expanduser("~"))
        if not os.path.isdir("CloneLab-data"):
            os.makedirs("CloneLab-data")
        os.chdir("CloneLab-data")

    # Getter for authentication
    @property
    def authentication(self):
        return self._authentication

    # Setter for authentication
    @authentication.setter
    def authentication(self, authentication):
        allowed_methods = ['ssh', 'https']
        if authentication.lower() in allowed_methods:
            self._authentication = authentication.lower()
        else:
            sys.exit(f"{authentication} is not an allowed authorization method")

    # Getter for kind
    @property
    def kind(self):
        return self._kind

    # Setter for kind
    @kind.setter
    def kind(self, kind):
        allowed_kinds = ['original', 'mirror']
        if kind.lower() in allowed_kinds:
            self._kind = kind.lower()
        else:
            sys.exit(f"Repository kind {kind} not allowed")

    # Getter for url
    @property
    def url(self):
        return self._url

    # Setter for url
    @url.setter
    def url(self, url):
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

    # Getter for mirror_username
    @property
    def mirror_username(self):
        return self._mirror_username

    # Setter for mirror_username
    @mirror_username.setter
    def mirror_username(self, mirror_username):
        self._mirror_username = mirror_username
