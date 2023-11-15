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
COPY ./ /root/CloneLab

# Copy example config from /root/CloneLab
WORKDIR /home/
RUN mkdir CloneLab
WORKDIR /home/CloneLab/
RUN mkdir config
RUN cp /root/CloneLab/config.csv.example /home/CloneLab/config/config

# Configure git
WORKDIR /home/CloneLab/
RUN git config --global user.name "chirmstream"
RUN git config --global user.email "dextergbarney@gmail.com"

# Run CloneLab
WORKDIR /home/CloneLab/config/
CMD ["python3", "/root/CloneLab/clonelab.py", "/home/CloneLab/config/config"]