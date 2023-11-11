import git


original_url = "https://github.com/chirmstream/CloneLab.git"

mirror_url = "https://github.com/chirmstream/CloneLab-Testing.git"
#mirror_url = "https://git.nasdex.net/chirmstream/clonelab-testing.git"

github_personal_access_token = "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"
gitlab_token = "glpat-ZsF8Ff4mLyWyaMs_XsjW"

repo = git.Repo(original_url, mirror_url)
repo.get()
repo.set_mirror_login(github_personal_access_token)
repo.sync()
repo.add()
repo.commit("this is a test commit")
repo.push()