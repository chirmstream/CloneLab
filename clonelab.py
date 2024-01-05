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

    # Import/Generate SSH keys and config
    os.chdir("..")
    os.chdir("ssh-config")
    print("Checking for SSH keys")
    ssh_files = []
    for file in os.listdir():
        ssh_files.append(file)
    if "id_ed25519" in ssh_files and "id_ed25519.pub" in ssh_files:
        print("Existing SSH keys found, importing...")
        with open("id_ed25519", "r") as file:
            ssh_private_key = file.readlines()
        with open("id_ed25519.pub", "r") as file:
            ssh_public_key = file.readlines()
        if ssh_key_import(ssh_private_key, ssh_public_key) != True:
            sys.exit("Error importing SSH keys")
        print("SSH Key imported...")
    else:
        print("Generating new SSH keys")
        user_path = os.path.expanduser("~")
        if os.path.exists(f"{user_path}/.ssh"):
            pass
        else:
            os.mkdir(f"{user_path}/.ssh")
        subprocess.run(['ssh-keygen', '-t', 'ed25519', '-C', 'clonelab', '-f', '~/.ssh/ed25519', '-q', '-N', '""'])
        user_path = os.path.expanduser("~")
        with open(f"{user_path}/id_ed25519", "r") as file:
            private_key = file.readlines()
            with open("id_ed25519", "w") as file:
                file.write(private_key)
        with open(f"{user_path}/id_ed25519.pub", "r") as file:
            public_key = file.readlines()
            with open("id_ed25519.pub", "w") as file:
                file.write(public_key)
        print('Generated keys saved to "ssh-config", please add public key to git repository...')
    print("Checking for SSH config")
    if "config" in ssh_files:
        print("SSH config found")
        with open("config", "r") as file:
            config = file.readlines()
        if ssh_config_import(config) != True:
            sys.exit("Error importing SSH config")
        print("SSH config imported...")
    else:
        print("No SSH config found, using default")   

    #os.chdir("..")
    #subprocess.run('cp', './ssh-config', '~/.ssh/')
    #subprocess.run('chmod', '600', '~/.ssh/id_rsa')
    #subprocess.run('chmod', '600', '~/.ssh/id_rsa.pub')
    #subprocess.run('chmod', '700', '~/.ssh')

    # Sync mirror repors
    os.chdir("..")
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


def ssh_key_import(private_key, public_key):
    user_path = os.path.expanduser("~")
    if os.path.exists(f"{user_path}/.ssh"):
        with open("id_ed25519", "w") as file:
            for line in private_key:
                file.write(line)
        with open("id_ed25519.pub", "w") as file:
            for line in public_key:
                file.write(line)
    else:
        os.makedirs(f"{user_path}/.ssh")
        return ssh_key_import(private_key, public_key)
    return True


def ssh_config_import(config):
    user_path = os.path.expanduser("~")
    if os.path.exists(f"{user_path}/.ssh"):
        with open("config", "w") as file:
            for line in config:
                file.write(line)
    else:
        os.makedirs(f"{user_path}/.ssh")
        return ssh_config_import(config)
    return True


main()