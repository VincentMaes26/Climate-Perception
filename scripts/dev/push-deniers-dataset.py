import pandas as pd
import boto3
import s3fs
import hashlib
import json


bucketname = 'ops-vw-interns-climate-perception-tweets'

s3_client = boto3.client('s3')
dataset = pd.read_csv('../datasets/climate-change-deniers/twitter_sentiment_data.csv')

s3_client.put_object(
    Bucket= bucketname,
    Body= dataset.to_csv(),
    Key= 'climate-change-deniers.csv',
)
