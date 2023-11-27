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
    -v /example-host/data:/root/CloneLab-data


## Python virtual enviroment
Create enviroment:

    python3 -m venv venv

Activate enviroment:

    . venv/bin/activate
