import git


original_url = "https://github.com/chirmstream/CloneLab.git"
mirror_url = "https://github.com/chirmstream/CloneLab-Testing.git"
github_personal_access_token = "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"

repo = git.Repo(original_url, mirror_url)
repo.get()
repo.mirror_auth(github_personal_access_token)
repo.sync()
repo.add()
repo.commit("this is a test commit")
repo.push()