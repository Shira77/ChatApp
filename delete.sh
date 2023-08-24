#!/bin/bash

# Stop all running containers
docker stop $(docker ps -a -q)

# Remove all stopped containers
docker rm $(docker ps -a -q)

# Remove all images
docker rmi -f $(docker images -a -q)