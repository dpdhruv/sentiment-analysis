# General:
import tweepy  # To consume Twitter's API
import tweepy
import json
import pandas as pd
from scipy.misc import imread
import matplotlib as mpl
import csv
import matplotlib.pyplot as plt

import operator
from textblob import TextBlob
from textblob import Word
from textblob.sentiments import NaiveBayesAnalyzer



####input your credentials here
consumer_key = 'MfNcPjHk8NyWW0sIJbBwmus66'
consumer_secret = '9Ll9sR7RzSuecPs0ezhtbP6T8BkGLiqXySNIa52Q67HbuqXn4s'
access_token = '960842445784219653-ef61yDcIObhIJnnm830wpA5UveeXR1C'
access_token_secret = 'Ku8GtcSrsUOuQqpbCb7ewmjbq10LmgBopBJ2LZ3kVlCNE'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret) #Interacting with twitter's API
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API (auth) #creating the API object


# Extracting Tweets
results = []
for tweet in tweepy.Cursor(api.search, q='millennials', lang="en").items(2000):
    results.append(tweet)

print(type(results))
print(len(results))


def tweets_df(results):
    id_list = [tweet.id for tweet in results]
    data_set = pd.DataFrame(id_list, columns=["id"])

    data_set["text"] = [tweet.text for tweet in results]
    data_set["created_at"] = [tweet.created_at for tweet in results]
    data_set["retweet_count"] = [tweet.retweet_count for tweet in results]
    data_set["user_screen_name"] = [tweet.author.screen_name for tweet in results]
    data_set["user_followers_count"] = [tweet.author.followers_count for tweet in results]
    data_set["user_location"] = [tweet.author.location for tweet in results]
    data_set["Hashtags"] = [tweet.entities.get('hashtags') for tweet in results]

    return data_set


data_set = tweets_df(results)

# Remove tweets with duplicate text

text = data_set["text"]

for i in range(0, len(text)):
    txt = ' '.join(word for word in text[i].split() if not word.startswith('https:'))
    data_set.set_value(i, 'text2', txt)

data_set.drop_duplicates('text2', inplace=True)
data_set.reset_index(drop=True, inplace=True)
data_set.drop('text', axis=1, inplace=True)
data_set.rename(columns={'text2': 'text'}, inplace=True)

text = data_set["text"]

for i in range(0,len(text)):
    textB = TextBlob(text[i])
    sentiment = textB.sentiment.polarity
    data_set.set_value(i, 'Sentiment',sentiment)
    if sentiment <0.00:
        SentimentClass = 'Negative'
        data_set.set_value(i, 'SentimentClass', SentimentClass )
    elif sentiment >0.00:
        SentimentClass = 'Positive'
        data_set.set_value(i, 'SentimentClass', SentimentClass )
    else:
        SentimentClass = 'Neutral'
        data_set.set_value(i, 'SentimentClass', SentimentClass )