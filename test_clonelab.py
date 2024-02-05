import git
import os
import csv
import sys


def main():
    # Sync mirror repos
    with open("config.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames
        os.chdir("..")
        for row in reader:
            repo = git.Repo(row["original_repository"], "original")
            mirror_repo = git.Repo(row["mirror_repository"], "mirror")
            mirror_repo.clone(repo)

    print("CLoneLab finished!  All repositories have been mirrored.")
    print("Exiting")


main()