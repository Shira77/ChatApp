#!/bin/bash
docker build -t myimage .
docker run -d -p 5000:5000 myimage



#docker volume create my-volume
#run the container
#docker run -p 5000:5000 -v my-volume:/code my-chat-app
#ran the container with limit cpu and memory
#docker run -it --ulimits nproc=1 --memory=1G my-container

#ran the large Dockerfile
#docker run -it --ulimits nproc=1 --memory=2G my-container