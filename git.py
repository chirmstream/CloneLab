import subprocess
import os
import re


class Repo:
    # url should include ".git" at the end
    def __init__(self, url):
        self.url = url

        match = re.search(r"https://(?:www\.)?github.com/(.+)/(.+)\.git", self.url)
        if match:
            self.username = match.group(1)
            if self.username:
                self.name = match.group(2)

        self.local_dir = "repos" + "/" + self.username + "/" + self.name

    def clone(self):
        # Runs the 'git clone' command
        subprocess.run(['git', 'clone', self.url, self.local_dir])


repo = Repo("https://github.com/chirmstream/VerifiedCommits.git")
repo.clone()



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