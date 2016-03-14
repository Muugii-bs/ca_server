# -*- coding: utf-8 -*-
from TwitterSearch import *
import ssl
import json

access_tokens = [
{
    'consumer_key': '7HFrbrv0USzw0FDXLsMwDvbTv',
    'consumer_secret': 'ViAg8MNk5J6LerTKHHuktFZZuK99HyyS57EJ0Bm2Xj8RQoibTH',
    'access_token': '427258701-aLYh4LM8qNt4Gf0YUa6YJl9TM6q39KeRoUTmcrgB',
    'access_token_secret': '4oJE53HREIsHrvys8jqHZwkO4rxgZnJF56zbUeBpxKGtZ',
},
{
    'consumer_key': 'aOl1BInpmLq1N3pxSdxBx1cm4',
    'consumer_secret': 'DMXy2bnMbRb0LN3VIDhYaiEghXLzKgaaK2ZLXawYJRiGIynbYi',
    'access_token': '4844553456-nOgJQAdSupO32nAQbhfUzmCtAeAzrhDfSEJk9cH',
    'access_token_secret': 'DL8OFjP4chuncL1j6EacOA8SKjLu8PdlzrxNavNmmr9sT',
}]
    

try:
    tso = TwitterSearchOrder()
    tso.set_keywords(['東京大学', '東大', '#東京大学', '#東大', 'UTokyo', '#UTokyo', 'The University of Tokyo', 'Tokyo University'])
    for access_token in access_tokens:
        ts = TwitterSearch(
            consumer_key = access_token['consumer_key'],
            consumer_secret = access_token['consumer_secret'],
            access_token = access_token['access_token'],
            access_token_secret = access_token['access_token_secret'],
         )
        for tweet in ts.search_tweets_iterable(tso):
            #print('@%s tweeted: %s' % (tweet['user']['screen_name'], tweet['text']))
            tweet = json.dumps(tweet)
            print tweet
            with open('tweets.json', 'a') as fp:
                fp.write(tweet)

except TwitterSearchException as e:
    print(e)
