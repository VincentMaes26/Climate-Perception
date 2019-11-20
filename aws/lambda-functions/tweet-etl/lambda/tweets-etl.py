import pandas as pd
import datetime
import re
import boto3
import s3fs
import nltk
nltk.download('stopwords')
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords

# Getting raw data from bucket
bucketname = 'ops-vw-interns-climate-perception-tweets'
dataframe = pd.DataFrame(columns=('creation date', 'tweet',
                                  'username'))
s3 = boto3.resource('s3')

s3_tweets = s3.Bucket(bucketname).objects.filter(Prefix='raw-data/', Delimiter='/').all()
for file in s3_tweets:
    temp_df = pd.read_json('s3://{}/{}'.format(bucketname, file.key))
    dataframe = dataframe.append(temp_df, sort=False, ignore_index=True)

# Removing bad rows
pattern = 'climate change|climatechange|global warming|globalwarming'
dataframe = dataframe[dataframe.tweet.str.contains('(?i)'+pattern)]

# Cleaning
stop_words = set(stopwords.words('english'))
def clean_tweet(tweet):
    processed_tweet=''
    for word in tweet.split():

        #Remove stopwords
        if not word in stop_words:

            # Removing URL from tweet
            processed_word = re.sub('([^0-9A-Za-z \t])|(\w+:\/\/\S+)', ' ', word)

            # remove all single characters
            processed_word = re.sub('\s+[a-zA-Z]\s+', ' ', processed_word)

            # Remove single characters from the start
            processed_word = re.sub('\^[a-zA-Z]\s+', ' ', processed_word)

            # Substituting multiple spaces with single space
            processed_word = re.sub('\s+', '', processed_word, flags=re.I)

            # Removing prefixed 'b'
            processed_word = re.sub('^b\s+', '', processed_word)

            # Removing &amp
            processed_word = re.sub('&amp', '&', processed_word)
            processed_word = re.sub('amp', '', processed_word)

            # Removing breaks
            processed_word = re.sub('<br/>', '', processed_word)

            # converts to lower
            processed_word = processed_word.lower()

            processed_tweet= processed_tweet+' '+processed_word

    return processed_tweet

tweets_text = [format_tweet(tweet) for tweet in dataframe['tweet']]

# Creating output dataframe with added label, sentiment polarity and word count column
def get_sentiment(polarity):
    if polarity > 0:
        return 'positive'
    if polarity == 0:
        return 'neutral'
    else:
        return 'negative'

word_count = [len(tweet.split()) for tweet in dataframe_tweets]

polarity_tweets = [round(sid.polarity_scores(tweet)['compound'], 2)
                   for tweet in tweets_text]

sentiment_tweets = [get_sentiment(polarity) for polarity in polarity_tweets]

dataframe['word count'] = word_count
dataframe['polarity'] = polarity_tweets
dataframe['sentiment'] = sentiment_tweets

# Posting transformed dataset to s3
s3 = boto3.client('s3')
temp_json = dataframe.to_dict(orient = 'records')
temp_json = json.dumps(temp_json, default=str)
s3_client.put_object(
    Bucket= bucketname,
    Body= temp_json,
    Key= 'clean-data/'+filename,
    ContentType = 'application/json'
)
