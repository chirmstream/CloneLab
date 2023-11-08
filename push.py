import subprocess
import os

# Replace these with your own values
repository_path = 'repos/'
remote_name = "origin"
branch_name = "main"  # Replace with the name of your branch

# Push the code to the remote repository
subprocess.run(["git", "push", remote_name, branch_name], cwd=repository_path)
