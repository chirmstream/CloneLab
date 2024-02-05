import os
import sys
import subprocess

# Export example files to their respective paths
def export_examples(cwd):
    user_path = os.path.expanduser("~")
    example_files = {
        'config' : f"{user_path}/config/config.csv",
        'git_config' : f"{user_path}/config/git_config.csv",
        'known_hosts' : f"{user_path}/ssh-config/known_hosts",
        'ssh_config' : f"{user_path}/ssh-config/config",
    }
    for example_file in example_files:
        if os.path.isfile(example_file):
            pass
        else:
            save_file(example_file, cwd)
    
    
    
    
#def export_keys(cwd):


def save_file(file, cwd):
    path = file['config']
    name = 'config'
    subprocess.run(['cp', f'{cwd}/rest_of_path/config', path])