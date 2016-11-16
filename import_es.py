# -*- coding: utf-8 -*-
from config     import db_config 
from datetime   import datetime 
from utils      import es_max_id

import pymysql as db
import json 
import os
import sys

conn    = db.connect(**db_config)
cursor  = conn.cursor()

def create_bulk_files():
    sql = "SELECT id,clan,tweet FROM tweets WHERE id>%s"
    id = es_max_id()
    cursor.execute(sql % id)
    for num,row in enumerate(cursor):
        if num % 20000 == 0:
            file_name = 'bulk_' + str(num)
            open(file_name, 'w').close()
        index = {'index': {'_index': 'ca1', '_type': 'tweets', '_id': row[0]}}
        data  = get_data(row[0], row[1], json.loads(row[2]))
        with open(file_name, 'a') as fp:
            fp.write(json.dumps(index) + '\n')
            fp.write(json.dumps(data) + '\n')

def convert_date(tmp):
    tmp = ' '.join([x for i,x in enumerate(tmp.split()) if i != 4])
    tmp = datetime.strptime(tmp, '%a %b %d %H:%M:%S %Y')
    tmp = datetime.strftime(tmp, '%Y-%m-%d %H:%M:%S')
    return tmp

def get_data(id, clan, tweet):
    data = {
        'id'                        : id,
        'user_clan_name'            : clan,
        'created'                   : convert_date(tweet['created_at']),
        'text'                      : tweet['text'],
        'favorite_count'            : tweet['favorite_count'],
        "retweet_count"             : tweet['retweet_count'],
        "retweeted"                 : tweet['retweeted'],
        "user_created"              : convert_date(tweet['user']['created_at']),
        "user_description"          : tweet['user']['description'],
        "user_followers_count"      : tweet['user']['followers_count'],
        "user_friends_count"        : tweet['user']['friends_count'],
        "user_name"                 : tweet['user']['name'],
        "user_screen_name"          : tweet['user']['screen_name'] 
    }
    if 'retweeted_status' in tweet:
        data['re_st_created']                 = convert_date(tweet['retweeted_status']['created_at'])
        data['re_st_favorite_count']          = tweet['retweeted_status']['favorite_count']
        data['re_st_retweet_count']           = tweet['retweeted_status']['retweet_count'] 
        data['re_st_retweeted']               = tweet['retweeted_status']['retweeted']
        data['re_st_text']                    = tweet['retweeted_status']['text']
        data['re_st_user_created']            = convert_date(tweet['retweeted_status']['user']['created_at'])
        data['re_st_user_description']        = tweet['retweeted_status']['user']['description']
        data['re_st_user_followers_count']    = tweet['retweeted_status']['user']['followers_count']
        data['re_st_user_friends_count']      = tweet['retweeted_status']['user']['friends_count']
        data['re_st_user_name']               = tweet['retweeted_status']['user']['name']
        data['re_st_user_screen_name']        = tweet['retweeted_status']['user']['screen_name']
    return data


def import_bulk_files():
    cmd = "curl -s -XPOST localhost:9200/_bulk --data-binary \"@%s\" > /dev/null"
    cmv = "rm %s"
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for f in files:
        if f.startswith('bulk_'):
            print("Importing file.....", f)
            os.system(cmd % f)
            os.system(cmv % f)

if __name__ == '__main__':
    create_bulk_files()
    import_bulk_files()
