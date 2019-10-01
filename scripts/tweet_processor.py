import re
import tweet_scraper

# Preprocessing of tweet texts
def format_tweet(tweet):
    processed_tweet=""
    for word in tweet.full_text.split():
        # Removing URL from tweet
        processed_word = re.sub(r'([^0-9A-Za-z \t])|(\w+:\/\/\S+)', ' ', word)
        
        # Remove all the special characters
        #processed_word = re.sub(r'\W', '', processed_word)
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

if __name__ == "__main__":
    tweets = tweet_scraper.get_tweets()