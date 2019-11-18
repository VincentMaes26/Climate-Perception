import pandas as pd
import boto3
import s3fs
import time
import re

BUCKET = 'ops-vw-interns-climate-perception-tweets'

s3 = boto3.resource('s3')
s3_client = boto3.client('s3')
s3_tweets = s3.Bucket(BUCKET).objects.filter(Prefix='objects/tweets', Delimiter='/').all()

for file in s3_tweets:
    try:
        filename = file.key.split('/')[1]
        filename = filename.split('.')[0]
        temp_df = pd.read_json('s3://{}/{}'.format(BUCKET, file.key))
        csv = temp_df.to_csv()
        s3_client.put_object(
            Bucket= BUCKET,
            Body= csv,
            Key= 'csv-objects/'+filename +'.csv',
        )
        print('{} has been moved'.format(filename))
    except Exception as e:
        print(e)
        raise e
