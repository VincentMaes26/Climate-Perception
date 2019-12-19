import pandas as pd
import datetime
import re
import boto3
import s3fs
import nltk
import json
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords 
stop_words = set(stopwords.words('english'))

# Getting raw data from bucket
BUCKETNAME = 'ops-vw-interns-climate-perception-tweets'
TODAY = datetime.datetime.today().strftime('%Y-%m-%d')

dataframe = pd.DataFrame(columns=('creation date', 'tweet',
                                  'username'))

s3_client = boto3.client('s3')

raw_tweets = s3_client.list_objects_v2(Bucket=BUCKETNAME, Prefix='raw-data/'+TODAY+'/')['Contents']
if raw_tweets == None:
    print('Something has gone wrong trying to read s3 bucket')
else:
    print("raw-data contains "+ str(len(raw_tweets))+ " objects.")

# Cleaning function
stop_words = set(stopwords.words('english'))
def clean_tweet(tweet):
    processed_tweet=''
    for word in tweet.split():

        #Remove stopwords
        if not word in stop_words:

            # Removing URL from tweet
            processed_word = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', ' ', word)

            # remove all single characters
            processed_word = re.sub(r'\s+[a-zA-Z]\s+', ' ', processed_word)

            # Remove single characters from the start
            processed_word = re.sub(r'\^[a-zA-Z]\s+', ' ', processed_word)

            # Substituting multiple spaces with single space
            processed_word = re.sub(r'\s+', '', processed_word, flags=re.I)

            # Removing prefixed 'b'
            processed_word = re.sub(r'^b\s+', '', processed_word)

            # Removing &amp
            processed_word = re.sub('&amp', '&', processed_word)
            processed_word = re.sub('amp', '', processed_word)

            # Removing breaks
            processed_word = re.sub('<br/>', '', processed_word)

            # converts to lower
            processed_word = processed_word.lower()

            processed_tweet= processed_tweet+' '+processed_word

    return processed_tweet

# Posting transformed dataset to s3
try:
    for file in raw_tweets:
        filename = file['Key'].split('/')[2]
        print(filename)
        temp_df = pd.read_json('s3://{}/{}'.format(BUCKETNAME, file['Key']))
        # cleaning
        temp_df['tweet'] = [clean_tweet(tweet) for tweet in temp_df['tweet']]
        # Removing bad rows
        pattern = 'climate change|climatechange|global warming|globalwarming'
        temp_df = temp_df[temp_df.tweet.str.contains('(?i)'+pattern)]
        print(temp_df.info())
        temp_json = temp_df.to_dict(orient = 'records')
        temp_json = json.dumps(temp_json, default=str)
        s3_client.put_object(
            Bucket= BUCKETNAME,
            Body= temp_json,
            Key= 'clean-data/'+TODAY+'/'+filename,
            ContentType = 'application/json'
        )

except Exception as e:
    print("Something has gone wrong trying to write to the s3 bucket.\n"+str(e))
