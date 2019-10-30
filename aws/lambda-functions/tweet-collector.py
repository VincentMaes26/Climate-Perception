import tweepy
import json
import re
import logging
import pandas as pd
import datetime
import boto3
import os
import sys
import hashlib

TARGET_BUCKET = 'ops-vw-interns-climate-perception-tweets'

TWEEPY_CONSUMER_KEY = os.getenv('tweepy_CONSUMER_KEY')
TWEEPY_CONSUMER_SECRET = os.getenv('tweepy_CONSUMER_SECRET')
TWEEPY_ACCESS_TOKEN = os.getenv('tweepy_ACCESS_TOKEN')
TWEEPY_ACCESS_SECRET = os.getenv('tweepy_ACCESS_SECRET')

DATETIME_NOW = datetime.datetime.now()

def init_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')

    # Sends output to console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    return logger

logger = init_logger()

# Returns true if retweet or reply
def is_retweet(tweet):
    if (hasattr(tweet, 'retweeted_status')):
        return True

# Gets tweets from api based on query words
def get_tweets():
    # Authenticates and connects to API
    auth = tweepy.OAuthHandler(TWEEPY_CONSUMER_KEY, TWEEPY_CONSUMER_SECRET)
    auth.set_access_token(TWEEPY_ACCESS_TOKEN, TWEEPY_ACCESS_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    today = datetime.date.today()

    query = "climate+change OR global+warming -filter:retweets -filter:replies"

    try:
        cursor = tweepy.Cursor(api.search, q= query, lang="en", since=today, tweet_mode='extended').items(300)
    except Exception as ex:
        logger.error(str(ex))

    return cursor

def create_dataframe():
    # Gets tweets based on query
    logger.info("Getting todays tweets with keywords = 'climate change' or 'global warming'. Limit = 300 tweets")
    cursor = list(get_tweets())

    print("Filtering out remaining retweets and None values")
    for tweet in cursor:
        if is_retweet(tweet):
            cursor.remove(tweet)

    tweets = list(filter(None, cursor))
    tweets = [tweet.full_text for tweet in tweets]
    # Gets username and creation date of tweet
    usernames = [tweet.user.name for tweet in cursor]
    usernames = [hashlib.md5(username.encode('utf-8')).hexdigest() for username in usernames]
    creation_dates = [tweet.created_at for tweet in cursor]
    creation_dates = list(filter(None, creation_dates))

    keywords = []
    for tweet in tweets:
        if "global warming" in tweet.lower() and "climate change" in tweet:
            keywords.append("Global warming & Climate change")
        elif "climate change" in tweet.lower():
            keywords.append("Climate change")
        elif "global warming" in tweet.lower():
            keywords.append("Global warming")


    list_for_dataframe = list(zip(keywords, tweets,usernames, creation_dates))
    df = pd.DataFrame(list_for_dataframe, columns=["keyword", "tweet","username", "creation date"])
    return df

# Exports tweets to csv in datasets folder
def convert_tweets_to_json():
    df = create_dataframe()
    if df.shape[0] == 0:
        logger.error("There has been an error. Dataframe tweets{}.json is empty".format(DATETIME_NOW))
        return None
    else:
        df_dict = df.to_dict(orient = 'records')
        df_json = json.dumps(df_dict, default=str)
        return df_json
        print("The dataframe tweets{}.json has been created. It contains {} tweets".format(DATETIME_NOW, len(df.index)))


def lambda_handler(event, context):
    body = convert_tweets_to_json()
    s3_client = boto3.client('s3')
    s3_client.put_object(
        Bucket = TARGET_BUCKET,
        Key = 'tweet-objects/tweets{}.json'.format(DATETIME_NOW),
        Body =  body,
        ContentType = 'application/json'
    )
