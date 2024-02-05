# CloneLab

Urls should include ".git" at the end

mirror repository needs to be public and initialized

Export/import gpg keys
https://www.jwillikers.com/backup-and-restore-a-gpg-key

gpg -o private.gpg --export-options backup --export-secret-keys ponder.stibbons@unseen.edu

gpg --import-options restore --import private.gpg


## ToDo
* Generate new SSH keys when no existing keys are found.
* Save new keys to host machine 
* Copy example files to host machine on startup
* Merge into 'main' branch
* Automatically start sync with CRON.


## Docker container mapping
docker run \
    -v /example-host/config:/home/CloneLab/config \
    -v /example-host/config/ssh:/home/CloneLab/config/ssh-config \
    -v /example-host/data:/root/CloneLab-data


## Python virtual enviroment
Create enviroment:

    python3 -m venv venv

Activate enviroment:

    . venv/bin/activate

## Configuring SSH
### SSH Keys
CloneLab will generate new SSH keys for you if none are provided.  If you already have keys, or prefer to generate your own simply add them to your ``ssh-config`` path.  Note that at this time CloneLab only supports ed25519 keys currently, although support may be expanded later.  You must name your private and public keys ``id_ed25519`` and ``id_ed25519.pub`` respectivly.  Make sure to add the public keys to your git server, otherwise they will not authenticate.  

Review GitHubs documentation for generating SSH keys and adding them to your account [here](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent).

### SSH Server Verification 
The ``known_hosts`` file tells your machine what SSH connections it can trust.  GitHub publishes their public keys [here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/githubs-ssh-key-fingerprints).  If you are using a different git server they should have their public keys published as well.  CloneLab has already taken GitHubs public SSH key fingerprints and put them into a default ``known_hosts`` file.  Simply add any new public keys to a new line for each server you are connecting to.

    ssh-keyscan github.com

To find the public SSH key for a server use the ``ssh-keyscan`` command.  If your git server is using a different port for SSH, designate the correct port with ``-p``.

    ssh-keyscan -p 22 github.com

If you would like to save the output to a file use ``>>[file_path]``.

    ssh-keyscan github.com >> ~/.ssh/known_hosts

### SSH ports
To specific SSH port you must create a ``config`` file and add it to the ``ssh-config`` path.  Here you can specify each ``Host`` followed by which ``Port`` to use.

    Host github.com
    Port 22


## Configuring GPG signed commits


## GitLab Notes
By default branch protection may hinder CloneLab's ability to push code.  Make sure "Allowed to force push" is enabled under ``Settings>Repository>Protected branches``.


## Prune docker build cache

    docker buildx prune
