import tweepy
import json
import re
import pandas as pd
import logging
import datetime


class TweetStreamListener(tweepy.StreamListener):

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_error disconnects the stream
            return False

    def on_status(self, status):
        print(status.text)


if __name__ == "__main__":

    # Gets authentication details from json file
    with open("twitter_credentials.json", "r") as file:
        creds = json.load(file)
    # Authenticates and connects to API
    auth = tweepy.OAuthHandler(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])
    auth.set_access_token(creds['ACCESS_TOKEN'], creds['ACCESS_SECRET'])
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    tweetStreamListener = TweetStreamListener()
    tweetStream = tweepy.Stream(auth= api.auth, listener=tweetStreamListener)  

    tweetStream.filter(track=['Climate change'], is_async=True) 

    [print(tweet.values) for tweet in list(tweetStream)]