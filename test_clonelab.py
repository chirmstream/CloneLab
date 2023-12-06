import git
import os
import csv


# Sync mirror repors
with open("config.csv", "r") as csvfile:
    reader = csv.DictReader(csvfile)
    fieldnames = reader.fieldnames
    os.chdir("..")
    for row in reader:
        repo = git.Repo(row["original_repository"], row["mirror_repository"])
        repo.get() # Need to setup to delete everything and reclone if it exists
        repo.set_mirror_login(row["mirror_password"])
        repo.sync()

print("CLoneLab finished!  All repositories have been mirrored.")
print("Exiting")