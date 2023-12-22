import git
import os
import csv
import subprocess


# Configure git
cwd = os.getcwd()
print(cwd)
print("Importing Git Configuration")
os.chdir("config")
with open("git_config.csv", "r") as git_config:
    reader = csv.DictReader(git_config)
    fieldnames = reader.fieldnames
    for row in reader:
        username = row["username"]
        email = row["email"]
        subprocess.run(['git', 'config', '--global', 'user.name', username])
        subprocess.run(['git', 'config', '--global', 'user.email', email])

# Import GPG key
subprocess.run(['gpg', '--import', '-ownertrust', 'private.gpg'])

# Import ssh keys
os.chdir("..")
os.chdir("ssh-config")
with open("put-keys-here", "w") as file:
    file.write("")
os.chdir("..")
subprocess.run('cp', './ssh-config', '~/.ssh/')
subprocess.run('chmod', '600', '~/.ssh/id_rsa')
subprocess.run('chmod', '600', '~/.ssh/id_rsa.pub')
subprocess.run('chmod', '700', '~/.ssh')

# Sync mirror repors
os.chdir("config")
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
