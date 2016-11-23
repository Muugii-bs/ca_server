import sys
import json
import re
import math
import numpy    as np
import pymysql  as db
import operator as op

from datetime import datetime
from config   import db_config
from utils    import load_annotation, get_tokens

conn = db.connect(**db_config)
cursor = conn.cursor()

exploits = load_annotation('exploits.tsv')
sql = "SELECT summary, exploit_type FROM vuln_analyze WHERE exploit_type IS NOT NULL AND entry_id IN ('%s')"
cursor.execute(sql % "','".join(list(exploits.keys())))
keywords = {}
stop_words = {}

with open('stop_words.tsv', 'r') as fp:
    for line in fp:
        stop_words[line.rstrip()] = 1

for row in cursor:
    words = get_tokens(row[0])
    for word in words:
        if not word in stop_words:
            if not word in keywords: keywords[word] = 1
            else: keywords[word] += 1

tmp = sorted(keywords.items(), key=op.itemgetter(1), reverse=True)
with open('keyword_master.txt', 'w') as fp:
    for pair in tmp:
        fp.write(pair[0] + '\t' + str(pair[1]) + '\n')


