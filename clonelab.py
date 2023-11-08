import subprocess

# Replace 'repository_url' with the URL of the Git repository you want to clone
repository_url = 'https://github.com/chirmstream/transcriber.git'

# Specify the destination directory where the repository will be cloned
destination_directory = 'repos/'

# Run the 'git clone' command
subprocess.run(['git', 'clone', repository_url, destination_directory])

# Mirror repository_url
#mirror_url = 'https://git.nasdex.net/chirmstream/transcriber.git'

#subprocess.run(['git', 'commit', destination_directory, -S -m "test commit"])
