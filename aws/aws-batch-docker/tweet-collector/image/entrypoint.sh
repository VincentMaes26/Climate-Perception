#!/usr/bin/env bash

aws s3 cp s3://ops-vw-interns-climate-perception-tweets/tweet-collector.zip . && unzip tweet-collector.zip && python tweet-collector.py