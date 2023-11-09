import git


original_url = "https://github.com/dhouck/anti-creeper-grief.git"
mirror_url = "https://github.com/chirmstream/CloneLab-Testing.git"

github_personal_access_token = "token"

repo = git.Repo(original_url, mirror_url)
repo.clone()

repo.mirror_auth(github_personal_access_token)
