from config     import configs, db_config
from datetime   import datetime
from pprint     import pprint
from utils      import Line

import pymysql  as db
import numpy    as np
import operator
import nltk 
import pickle
import sys
import json
import re
#{{{
black_list = [',', '.', ';', ':', '-', '~', '_', '?', '!', 'the', 'in', 
              'on', 'at', 'a', 'an', 'does', 'do', 'allows', 'allow', 
              'attackers', 'attacker', 'remote', 'by', 'with', 'through', 
              'or', 'is', 'are', 'to', 'as', 'without', 'via', 'of', 'and',
              'have', 'has', 'had', 'must', 'should', ')', '(', ']', '[',
              '{', '}', "''", "'", '"', '""', "``", '`', 'not', '..', ',,', 
              '.,', ',.', '--', '~~', '::', ';;', '+', '++', 'than', 'other',
              'it', 'its', 'for', 'along', 'be', 'it\'s', 'these', 'this',
              'these', 'those', 'into', "'s"]
conn = db.connect(**db_config)
cursor = conn.cursor()
#}}}
def get_tokens(text):
    tokens = nltk.word_tokenize(text)
    tokens = [x.lower() for x in tokens]
    tokens = list(set(tokens) - set(black_list))
    return tokens

def fetch_label(_text, exploit_db_id, flag):
    label_map = {
        'webapps': 0,
        'dos'    : 1,
        'local'  : 2,
        'remote' : 3
    }
    if flag == 'core':
        cursor.execute('SELECT type FROM vuln_exploit_fetched WHERE exploit_db_id=%s' % exploit_db_id)
        tmp = cursor.fetchone()
        if tmp:
            _text = tmp[0]
    label = [0] * 4
    if _text in label_map:
        label[label_map[_text]] = 1
    return label 

def load_annotation(file_name):
    res = {}
    with open(file_name, 'r') as fp:
        for line in fp:
            line            = line.rstrip().split('\t')
            exploit_db_id   = line[0].split(':')[1]
            cve_ids         = line[1].split()
            for cve in cve_ids:
                res[cve] = exploit_db_id
    return res

def fetch_layer(_text):
    re_obj = re.search(r'(cpe:/)(a|o|h)(.*)', _text, re.M|re.I)
    if re_obj: return re_obj.group(2)
    else: return None

def fetch_layer_sum(_text):
    _json = json.loads(_text)
    res = {'o': 0, 'h': 0, 'a':0}
    for item in _json:
        tmp = fetch_layer(item)
        if tmp: res[tmp] += 1
    return max(res.items(), key=operator.itemgetter(1))[0]

def load_score_master():
    SCORES = {}
    query = "SELECT metric_name, level_name, danger_level FROM vuln_score_new"
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        if not row[0] in SCORES: SCORES[row[0]] = {}
        SCORES[row[0]][row[1]] = float(row[2])
    return SCORES

class Line:
    
    def __init__(self, file_name):
        self.line = self.load_line(file_name)

    def load_line(self, file_name):
        with open(file_name, 'rb') as fp:
            res = pickle.load(fp)
        return res

    def get_line(self, id):
        return self.line[id]
