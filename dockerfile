FROM ubuntu:jammy
LABEL "author"="chirmstream"
LABEL version="0.1"

# Install requirements
RUN apt-get update && apt-get install -y \
    python3 \
    git \
    rsync \
    gpg

# Setup CloneLab (use git clone in future)
WORKDIR /root
RUN git clone -b rewrite https://github.com/chirmstream/CloneLab.git

# Copy example config from /root/CloneLab
WORKDIR /home/
RUN mkdir CloneLab
WORKDIR /home/CloneLab/
RUN mkdir config
RUN mkdir ssh-config
ADD https://raw.githubusercontent.com/chirmstream/CloneLab/rewrite/example_files/config.csv.example /home/CloneLab/config/config.example
ADD https://raw.githubusercontent.com/chirmstream/CloneLab/rewrite/example_files/git_config.csv.example /home/CloneLab/config/git_config.csv
ADD https://raw.githubusercontent.com/chirmstream/CloneLab/rewrite/example_files/ssh_config.example /home/CloneLab/ssh-config/config.example

# Run CloneLab
WORKDIR /home/CloneLab/
#ENTRYPOINT ["tail"]
#CMD ["-f","/dev/null"]
CMD ["python3", "/root/CloneLab/clonelab.py"]