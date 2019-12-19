import pandas as pd
import datetime
import re
import boto3
import s3fs
import nltk
import json
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

TODAY = datetime.datetime.today().strftime('%Y-%m-%d')
# Getting raw data from bucket
BUCKETNAME = 'ops-vw-interns-climate-perception-tweets'

s3_client = boto3.client('s3')

raw_tweets = s3_client.list_objects_v2(Bucket=BUCKETNAME, Prefix='clean-data/'+TODAY+'/')['Contents']
if raw_tweets == None:
    print('Something has gone wrong trying to read s3 bucket')
else:
    print("raw-data contains "+ str(len(raw_tweets))+ " objects.")

# Creating output dataframe with added label, sentiment polarity and word count column
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
            Key= 'labeled-data/'+TODAY+'/'+filename,
            ContentType = 'application/json'
        )

except Exception as e:
    print("Something has gone wrong trying to write to the s3 bucket.\n"+str(e))
