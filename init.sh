#!/bin/bash

docker build -t my-chat-app .

docker run -p 5000:5000 my-chat-app
