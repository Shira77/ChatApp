#!/bin/bash

# Stop all running containers
docker stop $(docker ps -a -q)

# Remove all stopped containers
docker rm $(docker ps -a -q)

# Remove all images
docker rmi -f $(docker images -a -q)

#build image
docker build -t myimage .

#run the image
docker run -d -p 5000:5000 myimage