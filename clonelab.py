import git


original_url = "https://github.com/chirmstream/repo.git"
mirror_url = "https://github.com/chirmstream/CloneLab-Testing.git"
github_personal_access_token = "token"

repo = git.Repo(original_url, mirror_url)
repo.clone()
repo.mirror_auth(github_personal_access_token)
repo.sync()
repo.add()
repo.commit("this is a test commit")
repo.push()