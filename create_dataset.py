import sys
import json
import re
import operator
import numpy as np
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
    query = "SELECT metric_name, level_name, danger_level FROM vuln_score_new"
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
        'webapps': 0,
        'dos'    : 1,
        'local'  : 2,
        'remote' : 3
    }
    label = [0] * 4
    if _text in label_map:
        label[label_map[_text]] = 1
    return label 

def create_dataset():
    dataset = []
    load_score_master()
    query = """SELECT software_list, score, access_vector, 
            access_complexity, authentication, confidentiality_impact, 
            integrity_impact, availability_impact, exploit_type
            FROM vuln_analyze 
            WHERE exploit_type IS NOT NULL 
            ORDER BY RAND() """
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
            tmp.append(label.index(1))
            dataset.append(tmp)
    cursor.close()
    conn.close()
    dataset = np.array(dataset)
    np.random.shuffle(dataset)
    np.save('data/dataset.npy', dataset)

if __name__ == '__main__':
    create_dataset()
