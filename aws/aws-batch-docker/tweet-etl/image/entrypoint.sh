#!/usr/bin/env bash

aws s3 cp s3://ops-vw-interns-climate-perception-tweets/tweet-etl.zip . && unzip tweet-etl.zip && python tweet-cleaning.py && python tweet-labeling.py