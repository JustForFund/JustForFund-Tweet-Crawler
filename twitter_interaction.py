import tweepy
import csv
import os

# Enter your Twitter API credentials here
consumer_key = os.environ['TWITTER_KEY']
consumer_secret = os.environ['TWITTER_SECRET']
access_token = os.environ['TWITTER_BEARER_ACCESS_TOKEN']
access_token_secret = os.environ['TWITTER_BEARER_TOKEN_SECRET']

# Authenticate with the Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def search_tweets(words_list):
    # Define the keywords or hashtags you want to search for
    keywords = ["data science", "#datascience", "machine learning"]
    # Search for tweets containing the keywords
    tweets = tweepy.Cursor(api.search_tweets, q=' OR '.join(keywords), tweet_mode='extended', lang='en').items(100)
    print(tweets)
    for tweet in tweets:
        print(tweet)
    return tweets

search_tweets([])