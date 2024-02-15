# CloneLab
Logo Space


## ToDo
* Create Logo
* Update setting up dev enviroment to use ``setup.py``
* Complete ``test_clonelab.py``, and merge ``test.py`` into ``test_clonelab.py``


## About
CloneLab is made using Python.  Git commands are done using the ``subprocesses`` module in python, and git authentication works with both HTTPS and SSH.  Most git servers only allow HTTPS for cloning public repositories so it is recommended to use SSH.  It is possible to authenticate using HTTPS with a personal access token as well.

CloneLab will require a ``GPG`` key to sign the commits it makes.  CloneLab will add to the commit message the original commit date, author, and message, along with a note that the commit was made using CloneLab.  The docker image does not contain any premade SSH or GPG keys, but will generate SSH keys for you.

I cannot speak to GitLabs security, since all the SSH, and GPG keys are stored in plain text.  I use it for cloning repositories to my self-hosted GitLab-CE server, since the community version does not have repository mirroring.  If this is extremely important you are probably better of using a different git server such as Gitea.

I recommend you use the docker image instead of running ``clonelab.py`` directly.  CloneLab configuration filepaths are admitidly, poorly setup and hard-coded in a few locations, so in my opinion you will have a better time using it inside a container.


## Docker container mapping
docker run \
    -v /example-host/config:/home/CloneLab/config \
    -v /example-host/config/ssh:/home/CloneLab/config/ssh-config \
    -v /example-host/data:/root/CloneLab-data


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
CloneLab will sign each commit using GPG keys.  CloneLab will not generate new GPG keys, you will have to generate them yourself and supply them to CloneLab in the ``config`` path.

Generate your GPG key using GitHubs [documentation](https://docs.github.com/en/authentication/managing-commit-signature-verification/generating-a-new-gpg-key).  After generating your keys you will need to export them into a ``private.gpg`` file.

    gpg -o private.gpg --export-options backup --export-secret-keys

To see a list of all your keys and then export a specific one use ``gpg --list-secret-keys`` and note which email is associated to the key you wish to export.

    gpg --list-secret-keys --keyid-format LONG

You should see an output similar to this:

    gpg: checking the trustdb
    gpg: marginals needed: 3  completes needed: 1  trust model: pgp
    gpg: depth: 0  valid:   3  signed:   0  trust: 0-, 0q, 0n, 0m, 0f, 3u
    gpg: next trustdb check due at 2023-09-21
    /Users/firstnamelastname/.gnupg/pubring.kbx
    --------------------------------------
    sec   rsa3072/E3F678E2082FFD28 2023-09-14 [SC] [expires: 2023-09-21]
        EF5B15FEAB93784D5A978136E3F678E2082FFD28
    uid                 [ultimate] test-name (no comment) <test-email@example.com>
    ssb   rsa3072/0AE917C1039735BD 2023-09-14 [E] [expires: 2023-09-21]

Export your chosen key

    gpg -o private.gpg --export-options backup --export-secret-keys <key-email>


## GitLab Users
By default branch protection may hinder CloneLab's ability to push code.  Make sure "Allowed to force push" is enabled under ``Settings>Repository>Protected branches``.

## Troubleshooting
No access to mirror repository.
* Test your access to the mirror repository.  Can you access it using SSH with the same credentials?

Cloning not working
* Make sure the mirror repository has been initialized.  There needs to be at least one commit for CloneLab to work.  It does not matter what branch it is on, although you should be aware the CloneLab uses the ``'main'`` branch.


## Contributing
To setup your dev enviroment you will need to create a python virtual enviroment and have docker installed.

Create enviroment:

    python3 -m venv venv

Activate enviroment:

    . venv/bin/activate

Install modules

    pip3 install pytest

I would sometimes have issues with VSCode/Docker using cached images locally on my system so any changes I made would not show up.  It may be helpful to remove all of your CloneLab images and clear the docker build cache.

    docker buildx prune


## License
CloneLab is released under the MIT license.  See [LICENSE](https://github.com/chirmstream/CloneLab/blob/main/LICENSE) for further details.