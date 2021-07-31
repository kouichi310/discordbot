#
#   key_tweepy.py
#
#                      Apr/26/2019
# ------------------------------------------------------------------
import  tweepy
import os
from dotenv import load_dotenv
from os.path import join, dirname

# ------------------------------------------------------------------
def key_tweepy_proc():
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    consumer_key = str(os.environ["CONSUMER_KEY"])
    consumer_secret = str(os.environ["CONSUMER_SECRET"])
    access_token = str(os.environ["ACCESS_TOKEN"])
    access_token_secret = str(os.environ["ACCESS_TOKEN_SECRET"])
#
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    return api
#
# ------------------------------------------------------------------