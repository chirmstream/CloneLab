import os
import sys
import subprocess
import re

# Export example files to their respective paths
def export_examples(cwd):
    user_path = os.path.expanduser("~")
    example_files = [
        f"{user_path}/config/config.csv",
        f"{user_path}/config/git_config.csv",
        f"{user_path}/ssh-config/known_hosts",
        f"{user_path}/ssh-config/config",
    ]
    for example_file in example_files:
        if os.path.isfile(example_file):
            pass
        else:
            save_file(example_file, cwd)
    

# Get file name and which config folder using regex in dest
def save_file(dest, cwd):
    match = re.search(r".+/((?:config)|(?:ssh-config))/((?:config.csv)|(?:git_config.csv)|(?:known_hosts)|(?:config))$", dest)
    folder, name = match.groups()
    if name == "config":
        name = "ssh_config"
    src = cwd + f"/example_files/{folder}/{name}.example"
    subprocess.run(['cp', src, dest])


# Export SSH keys used/generated so user can easily add public key to git server
def ssh_keys(user_path):
    private_key = f"{user_path}/.ssh/id_ed25519"
    public_key = f"{user_path}/.ssh/id_ed25519.pub"
    dest = f"{user_path}/ssh-config"
    subprocess.run(['cp', private_key, f"{dest}/id_ed25519"])
    subprocess.run(['cp', public_key, f"{dest}/id_ed25519.pub"])
