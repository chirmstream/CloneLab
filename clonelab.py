import pygit2

class MyRemoteCallbacks(pygit2.RemoteCallbacks):

    def transfer_progress(self, stats):
        print(f'{stats.indexed_objects}/{stats.total_objects}')


# GitHub repository URL
github_repo_url = "https://github.com/libgit2/pygit2"

# GitLab repository URL (your self-hosted GitLab)
gitlab_repo_url = "https://git.nasdex.net/chirmstream/pygit2"

# Clone the GitHub repository
print("Cloning pygit2")
repo = pygit2.clone_repository(github_repo_url, "repos/pygit2", bare=False, callbacks=MyRemoteCallbacks())

# Create a new commit to mirror the repository
#signature = pygit2.Signature("Your Name", "your.email@example.com")
#index = repo.index
#tree = index.write_tree(repo)
#message = "Mirror GitHub repository to GitLab"
#commit_oid = repo.create_commit("refs/heads/master", signature, signature, message, tree, [repo.head.target])

# Push the changes to your GitLab repository
#remote = repo.remotes.create("gitlab", gitlab_repo_url)
#credentials = pygit2.UserPass("username", "password")
#remote.credentials = credentials
#remote.push(["refs/heads/master"])

#print("Repository mirrored to GitLab successfully!")
