import git
import os


os.chdir("CloneLab-config")
cwd = os.getcwd()

with open("config", "r") as file:
    config = file
print(config)
print("script finished?")