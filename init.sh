#!/bin/bash
docker build -t my-chat-app .

docker volume create my-volume

docker run -p 5000:5000 -v my-volume:/code my-chat-app