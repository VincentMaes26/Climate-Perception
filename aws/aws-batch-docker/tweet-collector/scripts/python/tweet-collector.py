import tweepy
import json
import logging
import pandas as pd
import datetime
import boto3
import os
import sys
import hashlib
import base64
from botocore.exceptions import ClientError

TARGET_BUCKET = 'ops-vw-interns-climate-perception-tweets'

DATETIME_NOW = datetime.datetime.now()
TODAY = datetime.datetime.today().strftime('%Y-%m-%d')

def get_secret():

    secret_name = "tweet-collector/creds/tweepy"
    region_name = "eu-west-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
    # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    # We rethrow the exception by default.
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )

    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            return get_secret_value_response['SecretString']
        else:
            return base64.b64decode(get_secret_value_response['SecretBinary'])

def check_secret():
    secret = get_secret()
    secret_json = json.loads(secret)
    print(secret_json['CONSUMER_KEY'])


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
    credentials = get_secret()
    secret_json = json.loads(credentials)
    auth = tweepy.OAuthHandler(secret_json['CONSUMER_KEY'],
                                secret_json['CONSUMER_SECRET'])

    auth.set_access_token(secret_json['ACCESS_TOKEN'],
                                secret_json['ACCESS_SECRET'])

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

    list_for_dataframe = list(zip(tweets,usernames, creation_dates))
    df = pd.DataFrame(list_for_dataframe, columns=["tweet","username", "creation date"])
    return df

# Convert tweets to json
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

# Main function
if __name__ == "__main__":
    body = convert_tweets_to_json()
    s3_client = boto3.client('s3')
    s3_client.put_object(
        Bucket = TARGET_BUCKET,
        Key = 'raw-data/{}/tweets{}.json'.format(TODAY, DATETIME_NOW),
        Body =  body,
        ContentType = 'application/json'
    )
