import git
import os
import csv
import sys


def main():
    # Sync mirror repors
    with open("config.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames
        os.chdir("..")
        for row in reader:
            repo = git.Repo(row["original_repository"], "original")
            mirror_repo = git.Repo(row["mirror_repository"], "mirror")
            mirror_repo.clone(repo)
            repo.sync()

    print("CLoneLab finished!  All repositories have been mirrored.")
    print("Exiting")


def sync(repo, mirror_repo):
    valid = 1
    repo.get()
    mirror_repo.get()
    if repo.get_commits() == 1:
        pass
    else:
        sys.exit(f"Error parsing commit history for {repo.url}")
    if mirror_repo.get_commits() == 1:
        pass
    else:
        sys.exit(f"Error parsing commit history for {mirror_repo.url}")



main()