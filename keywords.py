import pymysql as db
import numpy as np
import operator as op
import sys

def run(attack_id, keyword):
    db_config = {
        'host':     '127.0.0.1',
        'port':     3306,
        'user':     'root',
        'passwd':   'root',
        'db':       'cnl'
    }
    conn = db.connect(**db_config)
    cursor = conn.cursor()
    keywords = keyword_master(cursor, attack_id, keyword)
    open('keywords_%s.tsv' % attack_id, 'w').close()
    with open('keywords_%s.tsv' % attack_id, 'a') as fp:
        for keyword in keywords:
            fp.write(keyword[0] + '\t' + str(keyword[1]) + '\n')
    cursor.close()
    conn.close()

def keyword_master(cursor, attack_id, keyword):
    stop_words = get_stop_words()
    sql = """
        SELECT content FROM ca_analyze
        WHERE attack_id=%s
        AND content LIKE '%%%s%%'
        """
    keywords = {}
    cursor.execute(sql % (attack_id, keyword))
    for row in cursor:
        words = row[0].split()
        for word in words:
            if word in stop_words: continue
            if not word in keywords: keywords[word] = 0
            keywords[word] += 1
    return sorted(keywords.items(), key=op.itemgetter(1), reverse=True)

def get_stop_words():
    stop_words = {}
    with open('stop_words.tsv', 'r') as fp:
        for line in fp:
            stop_words[line.rstrip()] = True
    return stop_words

def main():
    run(sys.argv[1], sys.argv[2])    

if __name__ == '__main__':
    main()

