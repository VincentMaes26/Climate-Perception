import tweepy
import json
import re
import pandas as pd
import logging
import datetime

logging.basicConfig(filename='{}.log'.format(str(datetime.datetime.now)),level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

# Returns true if retweet or reply
def isRetweet(tweet):
    if (hasattr(tweet, 'retweeted_status')):
        return True

# Preprocessing of tweet texts
def format_tweet(tweet):
    processed_tweet=""
    if not isRetweet(tweet):
        for word in tweet.full_text.split():
            
            # Removing URL from tweet
            processed_word = re.sub(r'([^0-9A-Za-z \t])|(\w+:\/\/\S+)', ' ', word)
            
            # Remove all the special characters
            processed_word = re.sub(r'\W', '', processed_word)

            # remove all single characters
            processed_word = re.sub(r'\s+[a-zA-Z]\s+', ' ', processed_word)

            # Remove single characters from the start
            processed_word = re.sub(r'\^[a-zA-Z]\s+', ' ', processed_word) 

            # Substituting multiple spaces with single space
            processed_word = re.sub(r'\s+', '', processed_word, flags=re.I)

            # Removing prefixed 'b'
            processed_word = re.sub(r'^b\s+', ' ', processed_word)

            # Converting to Lowercase
            processed_word = processed_word.lower()
            processed_tweet= processed_tweet+" "+processed_word

        return processed_tweet
            
    else:
        return

# Gets tweets from api based on query word
def get_tweets(start_date, end_date):
    # Gets authentication details from json file
    with open("twitter_credentials.json", "r") as file:
        creds = json.load(file)
    # Authenticates and connects to API
    auth = tweepy.OAuthHandler(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])
    auth.set_access_token(creds['ACCESS_TOKEN'], creds['ACCESS_SECRET'])
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    query = "climate change -filter:retweets"
    cursor = tweepy.Cursor(api.search, q= query, lang="en", since=start_date,  until=end_date , tweet_mode='extended').items(50000)
    # Filters out None objects
    cursor = list(filter(None,cursor))
    return cursor
    
# Exports tweets to csv in datasets folder    
def store_tweets_to_csv():
    logging.info("Process started")
    # Gets tweets based on query
    start_week = datetime.date.today() - datetime.timedelta(days=7)
    end_week = datetime.date.today()
    cursor = get_tweets(start_week, end_week)

    # Preprocesses the tweet texts
    tweets = [format_tweet(tweet) for tweet in cursor]
    tweets = list(filter(None, tweets))

    # Gets username and creation date of tweet
    usernames = [tweet.user.name for tweet in cursor]
    usernames = list(filter(None, usernames))
    
    creation_dates = [tweet.created_at for tweet in cursor]
    creation_dates = list(filter(None, creation_dates))
        
    list_for_dataframe = list(zip(tweets,usernames, creation_dates))

    df = pd.DataFrame(list_for_dataframe, columns=["tweet","username", "creation date"])
    start_week = datetime.date.today() - datetime.timedelta(days=7)
    month = start_week.month
    day = start_week.day
    if df.shape[0] == 0:
        print("There has been an error. Dataframe tweets_week{}-{} is empty".format(day, month))
    else:
        print("The dataframe tweets_week{}-{} has been stored in the datasets folder".format(day, month))
        df.to_csv(r'C:\stage\project\datasets\tweets_week{}-{}.csv'.format(day, month), index=False)

    logging.info("process ended")

if __name__ == "__main__":
    store_tweets_to_csv()




