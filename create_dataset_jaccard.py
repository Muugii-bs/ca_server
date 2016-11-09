import sys
import json
import re
import math
import operator
import numpy as np
import pymysql as db
from datetime import date 
from config import configs
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
NUM_CLASSES = configs['classes']
NUM_FACTORS = configs['factors']

def load_keyword_master():
    res = {}
    with open('isis_diff1', 'r') as fp:
        for num,line in enumerate(fp):
            line = line.rstrip().split()
            res[line[0]] = num
            if num == 1999: break
    return res

def create_dataset():
    dataset = []
    keyword_master = load_keyword_master()
    query = """
        SELECT content, date, date_orig FROM ca_analyze 
        WHERE attack_id=108 AND date_orig IS NOT NULL
        """
    cursor.execute(query)
    on, off = 0, 0
    for row in cursor.fetchall():
        tmp = [0.0] * 2000
        for word in row[0].split():
            if word in keyword_master: tmp[keyword_master[word]] += 1
        diff = (row[1] - row[2]).days
        if diff < 5: 
            tmp.append(1)
            on += 1
        elif diff > 10: 
            tmp.append(0)
            off += 1
        else: continue
        dataset.append(tmp)
    cursor.close()
    conn.close()
    print("on: %s, off: %s" % (str(on), str(off)))
    dataset = np.array(dataset)
    np.random.shuffle(dataset)
    np.save('data/dataset.npy', dataset)

if __name__ == '__main__':
    create_dataset()
