import pandas as pd
import datetime
import re
import boto3
import s3fs
import nltk
import json
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Getting raw data from bucket
BUCKETNAME = 'ops-vw-interns-climate-perception-tweets'

#s3 = boto3.resource('s3')
s3_client = boto3.client('s3')

raw_tweets = s3_client.list_objects_v2(Bucket=BUCKETNAME, Prefix='raw-data/')['Contents']
#raw_tweets = s3.Bucket(BUCKETNAME).objects.filter(Prefix='raw-data/', Delimiter='/').all()
if raw_tweets == None:
    print('Something has gone wrong trying to read s3 bucket')
else:
    print("raw-data contains "+ str(len(raw_tweets))+ " objects.")


def get_sentiment(polarity):
    if polarity > 0:
        return 'positive'
    if polarity == 0:
        return 'neutral'
    else:
        return 'negative'



# Posting transformed dataset to s3
try:
    for file in raw_tweets:
        filename = file['Key'].split('/')[2]
        print(filename)
        day = filename.split()[0]
        day = day.split('s')[1]
        temp_df = pd.read_json('s3://{}/{}'.format(BUCKETNAME, file['Key']))
        print(temp_df.info())


        word_count = [len(tweet.split()) for tweet in temp_df['tweet']]

        sid = SentimentIntensityAnalyzer()
        polarity_tweets = [round(sid.polarity_scores(tweet)['compound'], 2)
                            for tweet in temp_df['tweet']]

        sentiment_tweets = [get_sentiment(polarity) for polarity in polarity_tweets]
        temp_df['word count'] = word_count
        temp_df['polarity'] = polarity_tweets
        temp_df['sentiment'] = sentiment_tweets

        temp_json = temp_df.to_dict(orient = 'records')
        temp_json = json.dumps(temp_json, default=str)
        s3_client.put_object(
            Bucket= BUCKETNAME,
            Body= temp_json,
            Key= 'labeled-data/'+day+'/'+filename,
            ContentType = 'application/json'
        )

except Exception as e:
    print("Something has gone wrong trying to write to the s3 bucket.\n"+str(e))