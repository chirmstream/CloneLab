import git
import csv


with open("config.example", "r") as csvfile:
    #fieldnames = csv.DictReader(csvfile)
    #fieldnames = fieldnames.fieldnames
    #reader = csv.DictReader(csvfile, fieldnames=fieldnames)

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
