import git


original_url = "https://github.com/dhouck/anti-creeper-grief.git"
mirror_url = "https://github.com/chirmstream/CloneLab-Testing.git"

github_personal_access_token = "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"

repo = git.Repo(original_url, mirror_url)
repo.clone()

repo.mirror_auth(github_personal_access_token)

repo.sync()
#repo.add()
#repo.commit("commiting a public repo")

#repo.push("origin", "main")