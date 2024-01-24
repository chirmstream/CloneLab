# CloneLab

Urls should include ".git" at the end

mirror repository needs to be public and initialized

Export/import gpg keys
https://www.jwillikers.com/backup-and-restore-a-gpg-key

gpg -o private.gpg --export-options backup --export-secret-keys ponder.stibbons@unseen.edu

gpg --import-options restore --import private.gpg

## Docker container mapping
docker run \
    -v /example-host/config:/home/CloneLab/config \
    -v /example-host/config/ssh:/home/CloneLab/config/ssh \
    -v /example-host/data:/root/CloneLab-data


## Python virtual enviroment
Create enviroment:

    python3 -m venv venv

Activate enviroment:

    . venv/bin/activate

## GitLab Notes
By default branch protection may hinder CloneLab's ability to push code.  Make sure "Allowed to force push" is enabled under ``Settings>Repository>Protected branches``.

Selfhosted git servers and SSH keys
To authenticate with SSH you will need to supply a ``known_hosts`` file with your git server's public SSH key.  To easily find you SSH key you can use the ``ssh-keyscan`` command.

    ssh-keyscan github.com >> ~/.ssh/known_hosts

If you are not using the default SSH port (22) you can specify with ``-p``.

    ssh-keyscan -p 22 github.com >> ~/.ssh/known_hosts

## Prune docker build cache

    docker buildx prune
