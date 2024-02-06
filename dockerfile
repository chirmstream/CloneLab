FROM ubuntu:jammy

LABEL org.opencontainers.image.title=CloneLab
LABEL org.opencontainers.image.version=0.2
LABEL org.opencontainers.image.authors=chirmstream
LABEL org.opencontainers.image.source=https://github.com/chirmstream/CloneLab
LABEL org.opencontainers.image.licenses=MIT
LABEL org.opencontainers.image.description="TODO, add description"

# Install requirements
RUN apt-get update && apt-get install -y \
    python3 \
    git \
    rsync \
    gpg

# Setup CloneLab (use git clone in future)
WORKDIR /root
RUN git clone -b main https://github.com/chirmstream/CloneLab.git

# Copy example config from /root/CloneLab
WORKDIR /home/
RUN mkdir CloneLab
WORKDIR /home/CloneLab/
RUN mkdir config
RUN mkdir ssh-config

# TODO (move to script so it will do it before every start, regardless of container state)
#ADD https://raw.githubusercontent.com/chirmstream/CloneLab/rewrite/example_files/config.csv.example /home/CloneLab/config/config.example
#ADD https://raw.githubusercontent.com/chirmstream/CloneLab/rewrite/example_files/git_config.csv.example /home/CloneLab/config/git_config.csv
#ADD https://raw.githubusercontent.com/chirmstream/CloneLab/rewrite/example_files/ssh_config.example /home/CloneLab/ssh-config/config.example

# Run CloneLab
WORKDIR /home/CloneLab/
#ENTRYPOINT ["tail"]
#CMD ["-f","/dev/null"]
CMD ["python3", "-u", "/root/CloneLab/clonelab.py"]