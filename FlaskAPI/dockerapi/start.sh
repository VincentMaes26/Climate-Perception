#!/bin/bash

docker build -t "classifier.api" .
docker run -d -p 80:80 \
    --name="classifier.api" \
    -v $PWD:/app "classifier.api"
