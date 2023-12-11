import git
import os
import csv


# Sync mirror repors
with open("config.csv", "r") as csvfile:
    reader = csv.DictReader(csvfile)
    fieldnames = reader.fieldnames
    os.chdir("..")
    for row in reader:
        repo = git.Repo(row["original_repository"], original)
        mirror_repo = git.Repo(row["mirror_repository"], mirror)
        repo.sync()

print("CLoneLab finished!  All repositories have been mirrored.")
print("Exiting")