from utils import get_tokens

import pymysql as db
import numpy as np
import pickle
import json

db_config = {
    'user': 'root',
    'passwd': 'root',
    'host': 'localhost',
    'port': 3306,
    'db': 'cnl'
}
conn = db.connect(**db_config)
cursor = conn.cursor()

def jaccard():
    keywords = {}
    cursor.execute('SELECT summary FROM vuln_analyze')
    for row in cursor:
        tokens = get_tokens(row[0])
        for k1 in tokens:
            if not k1 in keywords: keywords[k1] = {}
            for k2 in tokens:
                if k1 == k2: continue
                if not k2 in keywords[k1]: keywords[k1][k2] = 0 
                keywords[k1][k2] += 1
    return keywords

def network(keywords, file_name):
    with open(file_name, 'w') as fp:
        for k1, k2s in keywords.items():
            for k2, cnt in k2s.items():
                fp.write(k1 + '\t' + k2 + '\t' + str(cnt) + '\n')

def load_keyword_line(file_name):
    keyword_line = {}
    with open(file_name, 'r') as fp:
        for num,line in enumerate(fp):
            if num == 0: continue 
            line = line.rstrip().split()
            keyword_line[line[0]] = np.asarray([float(x) for x in line[1:]])
    return keyword_line

def insert_vuln_line(keyword_line):
    res = {}
    sql = 'SELECT id, summary FROM vuln_analyze WHERE exploit_type IS NOT NULL'
    cursor.execute(sql)
    with open('vuln_line_labeled.pickle', 'wb') as fp:
        for row in cursor:
            tokens = get_tokens(row[1])
            vec  = np.mean([keyword_line[w] for w in tokens], axis=0) 
            res[row[0]] = vec
        pickle.dump(res, fp)

if __name__ == '__main__':
    #keywords = jaccard()
    #network(keywords, 'keywords.txt')
    keyword_line = load_keyword_line('keyword_line.txt')
    insert_vuln_line(keyword_line)
    cursor.close()
    conn.close()
