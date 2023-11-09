import git


original_url = "https://github.com/dhouck/anti-creeper-grief.git"
mirror_url = "https://github.com/chirmstream/CloneLab-Testing.git"

repo = git.Repo(original_url, mirror_url)

repo.add()
repo.commit("commiting a public repo")

repo.push("origin", "main")