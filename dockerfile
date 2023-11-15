FROM ubuntu:lunar-20231004
LABEL "author"="chirmstream"
LABEL version="x.x.x"

# Install requirements
RUN apt-get update && apt-get install -y \
    python3 \
    git \
    rsync \
    gpg

# Setup CloneLab (use git clone in future)
WORKDIR /root
RUN git clone https://github.com/chirmstream/CloneLab.git

# Copy example config from /root/CloneLab
WORKDIR /home/
RUN mkdir CloneLab
WORKDIR /home/CloneLab/
RUN mkdir config
RUN cp /root/CloneLab/config.csv.example /home/CloneLab/config/config

# Run CloneLab
WORKDIR /home/CloneLab/config/
CMD ["python3", "/root/CloneLab/clonelab.py", "/home/CloneLab/config/config"]