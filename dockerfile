# Build the image based on official ubuntu lunar image
FROM ubuntu:lunar-20231004

# Update ubuntu
RUN apt-get -y update

# Install git & python
RUN apt-get -y install git
RUN apt-get -y install python3

# Setup CloneLab (use git clone in future)
COPY ./ /home/ubuntu/CloneLab

WORKDIR /home/ubuntu/
RUN mkdir CloneLab-data
RUN mkdir CloneLab-config

# Setup persistant storage and docker volumes
#WORKDIR /home/ubuntu/CloneLab-data
#VOLUME ["/home/ubuntu/CloneLab-config", \
#        "/home/ubuntu/CloneLab-data"]

RUN cp /home/ubuntu/CloneLab/config.example /home/ubuntu/CloneLab-config/config

# Run python script
WORKDIR /home/ubuntu/
ENTRYPOINT ["python3", "/home/ubuntu/CloneLab/docker-run.py", "/home/ubuntu/CloneLab-config/config"]