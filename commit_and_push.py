import subprocess

# Replace these with your own values
repository_path = "repos/"
commit_message = "Your commit message"
remote_name = "origin"  # Replace with the name of your remote
branch_name = "main"  # Replace with the name of your branch

# Step 1: Add changes to the staging area (index) using 'git add'
subprocess.run(["git", "add", "."], cwd=repository_path)

# Step 2: Commit the changes using 'git commit'
subprocess.run(["git", "commit", "-m", commit_message], cwd=repository_path)

# Step 3: Push the committed changes to a remote repository using 'git push'
subprocess.run(["git", "push", remote_name, branch_name], cwd=repository_path)
