import tweepy
import json
import re
import pandas as pd
import logging
import datetime
import pymongo
import dns
from logger import init_logger


logger = init_logger()

# Returns true if retweet or reply
def is_retweet(tweet):
    if (hasattr(tweet, 'retweeted_status')):
        return True

# Gets tweets from api based on query word
def get_tweets():
    # Gets authentication details from json file
    with open("./credentials/twitter.json", "r") as file:
        creds = json.load(file)
    # Authenticates and connects to API
    auth = tweepy.OAuthHandler(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])
    auth.set_access_token(creds['ACCESS_TOKEN'], creds['ACCESS_SECRET'])
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    today = datetime.date.today()

    query = "climate+change OR global+warming -filter:retweets"

    try:
        cursor = tweepy.Cursor(api.search, q= query, lang="en", since=today, tweet_mode='extended').items(5000)
    except Exception as ex:
        logger.error(str(ex))
        
    return cursor

def create_dataframe():
    # Gets tweets based on query
    logger.info("Getting todays tweets with keywords = 'climate change' or 'global warming'. Limit = 5000 tweets")
    cursor = list(get_tweets())
    
    logger.info("Filtering out remaining retweets and None values")
    for tweet in cursor:
        if is_retweet(tweet):
            cursor.remove(tweet)

    tweets = list(filter(None, cursor))
    tweets = [tweet.full_text for tweet in tweets]
    # Gets username and creation date of tweet
    usernames = [tweet.user.name for tweet in cursor]
    usernames = list(filter(None, usernames))
    creation_dates = [tweet.created_at for tweet in cursor]
    creation_dates = list(filter(None, creation_dates))

    list_for_dataframe = list(zip(tweets,usernames, creation_dates))
    df = pd.DataFrame(list_for_dataframe, columns=["tweet","username", "creation date"])
    return df

# Exports tweets to csv in datasets folder    
def store_tweets_to_csv():
    df = create_dataframe()
    today = datetime.date.today()
    if df.shape[0] == 0:
        logger.error("There has been an error. Dataframe tweets{} is empty".format(today))
    else:
        df.to_csv(r'..\datasets\raw_data\tweets{}.csv'.format(today), index=False)
        logger.info("The dataframe tweets{} has been stored in the datasets folder. It contains {} tweets".format(today, len(df.index)))

    #logging.info("process ended")

# Export tweets to mongodb (cluster = Climate-Perception, database = textdata, collection = tweets)
def store_tweets_to_mongodb():

    df = create_dataframe()
    if df.shape[0] == 0:
        print("There has been an error. Dataframe is empty")
    else:
        print("Dataframe has been created and contains {} tweets".format(len(df.index)))

    # Setting up connection with mongodb & storing tweets
    with open("../credentials/mongodb.json", "r") as file:
        creds = json.load(file)
    try:
        client = pymongo.MongoClient("mongodb+srv://{0}:{1}@climate-perception-qpc1e.mongodb.net/test?retryWrites=true&w=majority".format(str(creds["USERNAME"]), str(creds["PASSWORD"])))
        db = client.textdata
        collection = db.tweets

        data = df.to_dict(orient='records') 
        collection.insert_many(data)
        print("Tweets succesfully stored in mongodb.")
    except Exception as ex:
        print("Could not connect to mongodb. Error: {}".format(ex))
  
if __name__ == "__main__":
    store_tweets_to_csv()
    #store_tweets_to_mongodb()



