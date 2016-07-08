import sys
import json
import operator
from itertools import izip
import mysql.connector as db
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

def date_diff(attack_date, publish_date):
    res = (attack_date - publish_date).days
    return int(res)

def create_hist():
    cursor.execute('SELECT id, entry_id, published_datetime, updated_datetime, score, access_vector, access_complexity, authentication, confidentiality_impact, integrity_impact, availability_impact, source, summary, ids FROM vuln_analyze')
    vulns = cursor.fetchall()
    for vuln in vulns:
        for attack_type, ids in json.loads(vuln[13]).iteritems():
            for id in ids:
                sql = 'INSERT IGNORE INTO vuln_ca_merge (entry_id, published_datetime, updated_datetime, score, access_vector, access_complexity, authentication, confidentiality_impact, integrity_impact, availability_impact, source, summary, attack_type, ca_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                cursor.execute(sql, (vuln[1], vuln[2], vuln[3], vuln[4], vuln[5], vuln[6], vuln[7], vuln[8], vuln[9], vuln[10], vuln[11], vuln[12], attack_type, id))

def main():
    create_hist()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()
