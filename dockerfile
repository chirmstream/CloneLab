FROM ubuntu:jammy

LABEL org.opencontainers.image.description="My container image"

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

# Run CloneLab
WORKDIR /home/CloneLab/
#ENTRYPOINT ["tail"]
#CMD ["-f","/dev/null"]
CMD ["python3", "-u", "/root/CloneLab/clonelab.py"]