import pymysql as db
import numpy as np
import operator as op
import json
import sys

def run(file_name):
    db_config = {
        'host':     '127.0.0.1',
        'port':     3306,
        'user':     'root',
        'passwd':   'root',
        'db':       'cnl'
    }
    conn = db.connect(**db_config)
    cursor = conn.cursor()
    with open(file_name, 'r') as fp:
        content = json.load(fp)
    write_keywords(cursor, content['content_ids_on'], content['content_ids_off'], file_name.split('.')[0] + '.tsv')
    cursor.close()
    conn.close()

def write_keywords(cursor, content_ids_on, content_ids_off, file_name):
    stop_words = get_stop_words()
    cursor.execute('SELECT content FROM ca_analyze WHERE id IN (%s)' % content_ids_on)
    res = {}
    for row in cursor:
        for word in row[0].split():
            if word in stop_words: continue
            if not word in res: res[word] = 0
            res[word] += 1
    res = sorted(res.items(), key=op.itemgetter(1), reverse=True)
    on = [x[0] for x in res]
    cursor.execute('SELECT content FROM ca_analyze WHERE id IN (%s)' % content_ids_off)
    res1 = {}
    for row in cursor:
        for word in row[0].split():
            if word in stop_words: continue
            if not word in res1: res1[word] = 0
            res1[word] += 1
    res1 = sorted(res1.items(), key=op.itemgetter(1), reverse=True)
    off = [x[0] for x in res1]
    with open('on_'+file_name, 'w') as fp:
        for pair in res:
            fp.write(pair[0] + '\t' + str(pair[1]) + '\n')
    with open('off_'+file_name, 'a') as fp:
        for pair in res1:
            fp.write(pair[0] + '\t' + str(pair[1]) + '\n')

def get_stop_words():
    stop_words = {}
    with open('stop_words.tsv', 'r') as fp:
        for line in fp:
            stop_words[line.rstrip()] = True
    return stop_words

def main():
    run(sys.argv[1])    

if __name__ == '__main__':
    main()
