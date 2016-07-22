import sys
import json
import re
import operator
import numpy as np
#import mysql.connector as db
import pymysql as db
from datetime import datetime
from pprint import pprint

db_config = {
    'host':	    '127.0.0.1',
    'port':	    3306,
    'user':	    'root',
    'password':	    'root',
    'database':	    'cnl',
    'autocommit':   True,
}

conn = db.connect(**db_config)
cursor = conn.cursor()

SCORES = {}

def load_score_master():
    query = "SELECT metric_name, level_name, danger_level FROM vuln_score"
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        if not row[0] in SCORES: SCORES[row[0]] = {}
        SCORES[row[0]][row[1]] = float(row[2]) 

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

def fetch_label(_text):
    """
    label: [availability, confidentiality, integrity, authenticity]
    """
    label_map = {
        'SQLi': 0,
        'DDoS': 1,
        'Malicious Code Injection': 0,
        'Targeted Attack': 2,
        'Defacement': 3,
        'Malware': 4,
        'Account Hijacking': 5,
        'other': 6,
        'unknown': 6
    }
    label = [0] * 3
    _json = json.loads(_text)
    for k,v in _json.items():
        k = k.lower()
        if len(v) > 0:
            #label[label_map[k]] = 1
            if k == 'sqli' or k == 'malicious code injection' or k == 'malware' or k == 'account hijacking':
                label[1], label[2] = 1, 1
            if k == 'ddos' or k == 'malware':
                label[0] = 1
            if k == 'targeted attack':
                label[1] = 1
            if k == 'defacement':
                label[2] = 1
        """
        if len(v) > 0: 
            if k == 'sqli' or k == 'malicious code injection' or k == 'malware':
                label[1], label[2] = 1, 1
            if k == 'ddos' or k == 'malware':
                label[0] = 1
            if k == 'targeted attack':
                label[1] = 1
            if k == 'defacement':
                label[2] = 1
            if k == 'account hijacking':
                label[3] = 1
        """
    return label

def create_dataset():
    dataset, labels = [], []
    load_score_master()
    query = """SELECT software_list, score, access_vector, 
            access_complexity, authentication, confidentiality_impact, 
            integrity_impact, availability_impact, ids
            FROM vuln_analyze ORDER BY RAND()"""
    cursor.execute(query)
    for row in cursor.fetchall():
        tmp = [None] * 8
        tmp[0] = float(SCORES['layer'][fetch_layer_sum(row[0])])
        tmp[1] = float(row[1])
        tmp[2] = float(SCORES['access_vector'][row[2]])
        tmp[3] = float(SCORES['access_complexity'][row[3]])
        tmp[4] = float(SCORES['authentication'][row[4]])
        tmp[5] = float(SCORES['confidentiality_impact'][row[5]])
        tmp[6] = float(SCORES['integrity_impact'][row[6]])
        tmp[7] = float(SCORES['availability_impact'][row[7]])
        label = fetch_label(row[8])
        if 1 in label:
            dataset.append(tmp)
            labels.append(label)
    cursor.close()
    conn.close()
    return np.array(dataset), np.array(labels)
