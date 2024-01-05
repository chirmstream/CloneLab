import git
import os
import csv
import sys
import subprocess


# Starting working directory is /home/CloneLab/
def main():
    # Configure git
    print("Importing git configuration")
    os.chdir("config")
    with open("git_config.csv", "r") as git_config:
        reader = csv.DictReader(git_config)
        fieldnames = reader.fieldnames
        for row in reader:
            username = row["username"]
            email = row["email"]
            subprocess.run(['git', 'config', '--global', 'user.name', username])
            subprocess.run(['git', 'config', '--global', 'user.email', email])
    print("Git import done...")


    # Import GPG key
    print("Importing GPG key")
    subprocess.run(['gpg', '--import', '-ownertrust', 'private.gpg'])
    print("GPG key importing done...")


    # Generating SSH Keys
    os.chdir("..")
    os.chdir("ssh-config")
    print("Checking for SSH keys")
    # Check for existing keys
    # If no keys exist, generate new keys
    # print("No SSH keys found, generating new")
        #subprocess.run(['ssh-keygen', '-t', 'ed25519', '-C', f{comment}])
        # Save keys to folder
    # print(Generated keys saved to (folder), please add public key to git repository..."")
    # Else: Import existing keys
    print("Existing SSH keys found, importing...")
    with open("config", "r") as file:
        config = file.readlines()
    with open("id_ed25519", "r") as file:
        ssh_private_key = file.readlines()
    with open("id_ed25519.pub", "r") as file:
        ssh_public_key = file.readlines()
    if ssh_setup(config, ssh_private_key, ssh_public_key) != True:
        sys.exit("Error setting up SSH")
    print("SSH Key imported...")
    print("No custom SSH config found, using default...")



    #os.chdir("..")
    #subprocess.run('cp', './ssh-config', '~/.ssh/')
    #subprocess.run('chmod', '600', '~/.ssh/id_rsa')
    #subprocess.run('chmod', '600', '~/.ssh/id_rsa.pub')
    #subprocess.run('chmod', '700', '~/.ssh')

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


def ssh_setup(config, private_key, public_key):
    user_path = os.path.expanduser("~")
    if os.path.exists(f"{user_path}/.ssh"):
        with open("config", "w") as file:
            for line in config:
                file.write(line)
        with open("id_ed25519", "w") as file:
            for line in private_key:
                file.write(line)
        with open("id_ed25519.pub", "w") as file:
            for line in public_key:
                file.write(line)
    else:
        os.makedirs(f"{user_path}/.ssh")
        return ssh_setup(config, private_key, public_key)
    return True


main()