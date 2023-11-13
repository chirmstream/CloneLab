import git
import os


#cwd = os.chdir(os.path.expanduser("~"))
#print(cwd)
os.chdir("..")
os.chdir("CloneLab-config")
cwd = os.getcwd()

with open("config", "r") as file:
    config = file
print(config)