import git
import os
import csv


os.chdir("CloneLab-config")

with open("config", "r") as csvfile:
    reader = csv.DictReader(csvfile)
    fieldnames = reader.fieldnames
    for row in reader:
        repo = git.Repo(row["original_repository"], row["mirror_repository"])
        repo.get()
        repo.set_mirror_login(row["mirror_password"])
        repo.sync()
        repo.add()
        repo.commit("this is a test commit")
        repo.push()


print(config)
print("script finished?")