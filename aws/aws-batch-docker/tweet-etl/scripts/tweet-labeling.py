import pandas as pd
import datetime
import re
import boto3
import s3fs
import nltk
import json
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer


# Getting raw data from bucket
BUCKETNAME = 'ops-vw-interns-climate-perception-tweets'

dataframe = pd.DataFrame(columns=('creation date', 'tweet',
                                  'username'))

s3_client = boto3.client('s3')

for obj in s3_client.list_objects_v2(Bucket=BUCKETNAME, Prefix='clean-data/')['Contents']:
        dataframe = pd.read_json('s3://{}/{}'.format(BUCKETNAME, obj['Key']))


# Creating output dataframe with added label, sentiment polarity and word count column
def get_sentiment(polarity):
    if polarity > 0:
        return 'positive'
    if polarity == 0:
        return 'neutral'
    else:
        return 'negative'

word_count = [len(tweet.split()) for tweet in dataframe['tweet']]

sid = SentimentIntensityAnalyzer()
polarity_tweets = [round(sid.polarity_scores(tweet)['compound'], 2)
                   for tweet in dataframe['tweet']]

sentiment_tweets = [get_sentiment(polarity) for polarity in polarity_tweets]

dataframe['word count'] = word_count
dataframe['polarity'] = polarity_tweets
dataframe['sentiment'] = sentiment_tweets

# Posting transformed dataset to s3
temp_json = dataframe.to_dict(orient = 'records')
temp_json = json.dumps(temp_json, default=str)
s3_client.put_object(
    Bucket= BUCKETNAME,
    Body= temp_json,
    Key= 'labeled-data/'+'dataset',
    ContentType = 'application/json'
)
