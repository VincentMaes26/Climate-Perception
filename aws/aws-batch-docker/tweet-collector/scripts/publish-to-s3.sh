#!/usr/bin/env bash
cd python
rm tweet-collector.zip
7Z.exe a -r \tweet-collector.zip *
aws s3 cp tweet-collector.zip s3://ops-vw-interns-climate-perception-tweets/tweet-collector.zip