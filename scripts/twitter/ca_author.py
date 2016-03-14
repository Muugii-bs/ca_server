# -*- coding: utf-8 -*-
from TwitterSearch import *
from pprint import pprint
import mysql.connector as db
import time
import json
import sys

class MySQLConverter(db.conversion.MySQLConverter):
    """ A mysql.connector Converter that handles Numpy types """

    def _float32_to_mysql(self, value):
        return float(value)

    def _float64_to_mysql(self, value):
        return float(value)

    def _int32_to_mysql(self, value):
        return int(value)

    def _int64_to_mysql(self, value):
        return int(value)

db_config = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': 'root',
        'database': 'cnl',
        'autocommit': True,
        'raise_on_warnings': True,
}
conn = db.connect(**db_config)
conn.set_converter_class(MySQLConverter)
cursor = conn.cursor()

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

CLAN_IDS = {
        'Anonymous': {
            'min_id': 232,
            'max_id': 308
        },
        'Zyklon': {
            'min_id': 309,
            'max_id': 311
        },
        'LizardSquad': {
            'min_id': 312,
            'max_id': 319
        },
        'DrSHA67': {
            'min_id': 320,
            'max_id': 320
        },
        'halifaxanon': {
            'min_id': 321,
            'max_id': 321
        }
}


def get_tweets(clan_name):
    try:
        cursor.execute('SELECT user_id, token_id FROM log WHERE clan=%s', (clan_name,))
        user_id, token_num = cursor.fetchall()[0]
        perform(token_num, clan_name, user_id)
    except TwitterSearchException as e:
        cursor.execute('SELECT user_id, token_id FROM log WHERE clan=%s', (clan_name,))
        user_id, token_num = cursor.fetchall()[0]
        perform((token_num + 1) % len(access_tokens), clan_name, user_id)
        print(e)

def perform(token_num, clan_name, user_id):
    while True:
        cursor.execute('UPDATE log SET user_id=%s, token_id=%s WHERE clan=%s', (user_id, token_num, clan_name))
        cursor.execute('SELECT name FROM accounts WHERE id=%s', (user_id,))
        user = cursor.fetchall()[0][0]
        get_tweet(token_num, user, clan_name)
        if user_id < CLAN_IDS[clan_name]['max_id']:
            user_id += 1
        else:
            cursor.execute('UPDATE log SET user_id=%s, token_id=%s WHERE clan=%s', (CLAN_IDS[clan_name]['min_id'], token_num, clan_name))
            sys.exit()

def get_tweet(token_num, user, clan):
    date = time.strftime('%Y-%m-%d %H:%M:%S')
    ts = TwitterSearch(
        consumer_key = access_tokens[token_num]['consumer_key'],
        consumer_secret = access_tokens[token_num]['consumer_secret'],
        access_token = access_tokens[token_num]['access_token'],
        access_token_secret = access_tokens[token_num]['access_token_secret'],
     )
    tso = TwitterUserOrder(user)
    for tweet in ts.search_tweets_iterable(tso):
        #print('@%s tweeted: %s' % (tweet['user']['screen_name'].encode('utf-8'), tweet['text'].encode('utf-8')))
        cursor.execute('INSERT IGNORE INTO tweets (date, name, clan, tweet) VALUES (%s, %s, %s, %s)', (date, user, clan, json.dumps(tweet),))

def main():
    get_tweets(sys.argv[1])
    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()
