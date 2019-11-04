import pandas as pd
import boto3
import s3fs
import hashlib
import json


bucketname = 'ops-vw-interns-climate-perception-tweets'

s3 = boto3.resource('s3')
s3_client = boto3.client('s3')
s3_tweets = s3.Bucket(bucketname).objects.filter(Prefix='tweet-objects/tweets', Delimiter='/').all()

for file in s3_tweets:
    filename = file.key.split('/')[1]
    temp_df = pd.read_json('s3://{}/{}'.format(bucketname, file.key))
    temp_json = temp_df.to_dict(orient = 'records')
    temp_json = json.dumps(temp_json, default=str)
    s3_client.put_object(
        Bucket= bucketname,
        Body= temp_json,
        Key= 'objects/'+filename,
        ContentType = 'application/json'
    )
