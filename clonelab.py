import git


original_url = "https://github.com/TheSpaghettiDetective/obico-server.git"
mirror_url = "https://github.com/chirmstream/CloneLab-Testing.git"
github_personal_access_token = "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"

repo = git.Repo(original_url, mirror_url)
repo.clone()
repo.mirror_auth(github_personal_access_token)
repo.sync()
repo.add()
repo.commit("commiting a public repo")
repo.push()