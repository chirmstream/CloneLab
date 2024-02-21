import git
import os
import csv
import sys
import subprocess
import load


# Starting working directory is /home/CloneLab/
def main():
    # Save default configuration files for user convience IF configs not provided
    user_path = os.path.expanduser("~")
    load.export_examples(f"{user_path}/CloneLab")

    # Configure git
    print("Importing git configuration")
    os.chdir("/home/CloneLab/config")
    with open("git_config.csv", "r") as git_config:
        reader = csv.DictReader(git_config)
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

    # Import/Generate SSH keys
    os.chdir("..")
    os.chdir("ssh-config")
    check_ssh_path()
    print("Checking for SSH keys")
    ssh_files = []
    for file in os.listdir():
        ssh_files.append(file)
    ssh_keys = key_search(ssh_files)
    if ssh_keys:
        print("Existing SSH keys found, importing...")
        ssh_private_key, ssh_public_key = ssh_read_keys()
        print("    SSH keys read from disk...")
        ssh_key_import(ssh_private_key, ssh_public_key)
        print("SSH keys imported...")
    else:
        print("No SSH keys found, generating...")
        ssh_private_key, ssh_public_key = ssh_generate_keys()
        print("Saving generated SSH keys to 'ssh-config', please add public key to git server")
        ssh_export_keys(ssh_private_key, ssh_public_key)

    # Import SSH configuration (optional)
    print("Checking for SSH config")
    ssh_config = ssh_config_search(ssh_files)
    if ssh_config:
        print("SSH config found")
        ssh_config = ssh_read_config("config")
        ssh_config_import(ssh_config)
        print("SSH config imported...")
    else:
        print("No SSH config found, using default")

    # Import SSH known hosts (optional)
    print("Checking for SSH known_hosts")
    hosts_known = ssh_hosts_search(ssh_files)
    if hosts_known:
        print("Found SSH known_hosts file, importing...")
        known_hosts = ssh_read_known_hosts()
        ssh_known_hosts_import(known_hosts)
    else:
        print("No known SSH hosts...")

    # Apply correct ownership and permission to SSH Keys
    print("Applying SSH ownership and permissions")
    user_path = os.path.expanduser("~")
    chmod(f"{user_path}/.ssh")
    
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

    # Export SSH keys
    #load.ssh_keys(user_path)
    print("Exiting")


def ssh_read_keys():
    path = "/home/CloneLab/ssh-config"
    with open(f"{path}/id_ed25519", "r") as file:
        ssh_private_key = file.readlines()
    with open(f"{path}/id_ed25519.pub", "r") as file:
        ssh_public_key = file.readlines()
    return ssh_private_key, ssh_public_key


def ssh_read_known_hosts():
    path = "/home/CloneLab/ssh-config"
    with open(f"{path}/known_hosts", "r") as file:
        known_hosts = file.readlines()
    return known_hosts


def ssh_key_import(private_key, public_key):
    user_path = os.path.expanduser("~")
    if os.path.exists(f"{user_path}/.ssh"):
        with open(f"{user_path}/.ssh/id_ed25519", "w") as file:
            for line in private_key:
                file.write(line)
        with open(f"{user_path}/.ssh/id_ed25519.pub", "w") as file:
            for line in public_key:
                file.write(line)
    else:
        os.makedirs(f"{user_path}/.ssh")
        return ssh_key_import(private_key, public_key)
    return True


def ssh_config_import(config):
    user_path = os.path.expanduser("~")
    if os.path.exists(f"{user_path}/.ssh"):
        with open(f"{user_path}/.ssh/config", "w") as file:
            for line in config:
                file.write(line)
    else:
        os.makedirs(f"{user_path}/.ssh")
        return ssh_config_import(config)
    return True


def ssh_known_hosts_import(known_hosts):
    user_path = os.path.expanduser("~")
    path = f"{user_path}/.ssh"
    with open(f"{path}/known_hosts", "w") as file:
        for line in known_hosts:
            file.write(line)


def key_search(ssh_files):
    if "id_ed25519" in ssh_files and "id_ed25519.pub" in ssh_files:
        return True
    else:
        return False


def ssh_hosts_search(ssh_files):
    if "known_hosts" in ssh_files:
        return True
    else:
        return False


def check_ssh_path():
    try:
        user_path = os.path.expanduser("~")
        ssh_path = f"{user_path}/.ssh"
    except:
        return 1
    if os.path.exists(ssh_path):
        pass
        return 0
    else:
        os.mkdir(ssh_path)
        return 0


def ssh_generate_keys():
    check_ssh_path()
    user_path = os.path.expanduser("~")
    path = f"{user_path}/.ssh/id_ed25519"
    password = ""
    subprocess.run(['ssh-keygen', '-t', 'ed25519', '-C', 'clonelab', '-f', path, '-q', '-N', password])
    user_path = os.path.expanduser("~")
    with open(f"{user_path}/.ssh/id_ed25519", "r") as file:
        private_key = file.readlines()
        with open("id_ed25519", "w") as file:
            for line in private_key:
                file.write(line)
    with open(f"{user_path}/.ssh/id_ed25519.pub", "r") as file:
        public_key = file.readlines()
        with open("id_ed25519.pub", "w") as file:
            for line in public_key:
                file.write(line)
    return private_key, public_key


def ssh_export_keys(private_key, public_key):
    path = "/home/CloneLab/ssh-config"
    with open(f"{path}/id_ed25519", "w") as file:
        for line in private_key:
            file.write(line)
    with open(f"{path}/id_ed25519.pub", "w") as file:
        for line in public_key:
            file.write(line)


def ssh_config_search(files):
    if "config" in files:
        return True
    else: 
        return False


def ssh_read_config(config):
    try:
        with open(f"/home/CloneLab/ssh-config/{config}", "r") as file:
            config = file.readlines()
        return config
    except:
        sys.exit("error importing ssh-config")


def chmod(ssh_path):
    subprocess.run(['chmod', '700', f'{ssh_path}'])
    subprocess.run(['chmod', '600', f'{ssh_path}/id_ed25519'])
    subprocess.run(['chmod', '644', f'{ssh_path}/id_ed25519.pub'])


if __name__ == "__main__":
    main()
    