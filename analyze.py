# -*- coding: utf-8 -*-
from config     import db_config 
from datetime   import datetime 
from utils      import es_search

import pymysql as db
import json 

conn    = db.connect(**db_config)
cursor  = conn.cursor()

def get_items(txt):
    tmp = txt.rstrip().lstrip().lower().split(',')
    return [x.rstrip().lstrip() for x in tmp]

def get_es(keyword):
    res = es_search(keyword, '2016-03-06 00:00:00', '2016-12-06 00:00:00')
    if res['hits']['total'] > 0: return res['hits']['hits']
    return None

def get_tweets():
    prefix = 'keywords/'
    sql    = "SELECT id,author,tags FROM ca_timeline_new WHERE id > 1571 AND except=0"
    cursor.execute(sql)
    for row in cursor:
        authors = get_items(row[1])
        targets = list(set(get_items(row[2])) - set(authors))
        for target in targets:
            res = get_es(target)
            if res:
                with open(prefix + str(row[0]) + '_tags_' + target + '.json', 'w') as fp:
                    json.dump(res, fp)
        for author in authors:
            res = get_es(author)
            if res:
                with open(prefix + str(row[0]) + '_author_' + author + '.json', 'w') as fp:
                    json.dump(res, fp)

if __name__ == '__main__':
    get_tweets()
