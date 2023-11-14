import git
import os
import csv


with open("config", "r") as csvfile:
    reader = csv.DictReader(csvfile)
    fieldnames = reader.fieldnames
    os.chdir("..")
    for row in reader:
        repo = git.Repo(row["original_repository"], row["mirror_repository"])
        repo.get()
        repo.set_mirror_login(row["mirror_password"])
        repo.sync()
        repo.add()
        repo.commit("CloneLab autocommit")
        repo.push()

print("script finished?")