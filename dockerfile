# Build the image based on official ubuntu lunar image
FROM ubuntu:lunar-20231004

# Update ubuntu
RUN apt-get -y update

# Install git & python
RUN apt-get -y install git
RUN apt-get -y install python3
RUN apt-get -y install rsync
RUN apt-get -y install gpg


# Setup CloneLab (use git clone in future)
COPY ./ /root/CloneLab

WORKDIR /home/
RUN mkdir CloneLab
WORKDIR /home/CloneLab/
RUN mkdir config

# Copy example config from /root/CloneLab
RUN cp /root/CloneLab/config.example /home/CloneLab/config/config

# Copy gpg key
#RUN cp /root/CloneLab/private.gpg /home/CloneLab/config/private.gpg

# Configure git
WORKDIR /home/CloneLab/
RUN git config --global user.name "chirmstream"
RUN git config --global user.email "dextergbarney@gmail.com"

# Import GPG key
#WORKDIR /home/CloneLab/config
#RUN gpg --import -ownertrust private.gpg

# Run python script and setup user
WORKDIR /home/CloneLab/config/

CMD ["python3", "/root/CloneLab/clonelab.py", "/home/CloneLab/config/config"]