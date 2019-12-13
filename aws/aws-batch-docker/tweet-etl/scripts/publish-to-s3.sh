#!/usr/bin/env bash
cd python
rm tweet-etl.zip
7Z.exe a -r \tweet-etl.zip *
aws s3 cp tweet-etl.zip s3://ops-vw-interns-climate-perception-tweets/tweet-etl.zip