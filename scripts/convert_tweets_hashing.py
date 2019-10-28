import pandas as pd
import boto3
import s3fs
import hashlib
import json


bucketname = 'ops-vw-interns-climate-perception-tweets'
dataframe = pd.DataFrame(columns=('creation date','keyword', 'tweet', 
                                  'username'))

s3 = boto3.resource('s3')
s3_client = boto3.client('s3')
s3_tweets = s3.Bucket(bucketname).objects.filter(Prefix='old-tweet-objects/tweets', Delimiter='/').all()

json_list = []

for file in s3_tweets:
    filename = file.key.split('/')[1]
    temp_df = pd.read_json('s3://{}/{}'.format(bucketname, file.key))
    temp_df['username'] = temp_df['username'].apply(lambda x : hashlib.md5(x.encode('utf-8')).hexdigest())
    temp_json = temp_df.to_dict(orient = 'records')
    temp_json = json.dumps(temp_json, default=str)
    s3_client.put_object(
        Bucket= bucketname,
        Body= temp_json,
        Key= 'tweet-objects/'+filename,
        ContentType = 'application/json'
    )
    




