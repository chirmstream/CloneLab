import subprocess

# Replace 'repository_url' with the URL of the Git repository you want to clone
repository_url = 'https://github.com/gitpython-developers/GitPython.git'

# Specify the destination directory where the repository will be cloned
destination_directory = 'repos/test'

# Run the 'git clone' command
subprocess.run(['git', 'clone', repository_url, destination_directory])
