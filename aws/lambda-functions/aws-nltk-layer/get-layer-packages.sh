#!/usr/bin/env bash

export PKG_DIR="python"

rm -rf ${PKG_DIR} && mkdir -p ${PKG_DIR}

sudo docker run --rm -v $(pwd):/home/vms/Documents/nltk-layer-aws -w /home/vms/Documents/nltk-layer-aws lambci/lambda:build-python3.7 \
  pip install -r requirements.txt --no-deps -t ${PKG_DIR}
