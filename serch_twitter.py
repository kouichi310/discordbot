#
#   search_word.py
#
#                       Apr/26/2019
# ------------------------------------------------------------------
import  sys
import  tweepy
from key_tweepy import key_tweepy_proc

# ------------------------------------------------------------------
api = key_tweepy_proc()
word = {"null":"null鯖"}
set_count = 1
def serch_tw(mess):
    results = api.search(q=word[mess], count=set_count)
    for result in results:
        username = result.user._json['screen_name']
        status_n = result._json['id']
        url_r = "https://twitter.com/" + username + "/status/" + str(status_n)
    return url_r
#
# ------------------------------------------------------------------