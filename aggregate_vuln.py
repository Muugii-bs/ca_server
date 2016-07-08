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
    cursor.execute('SELECT id, date, attack_type FROM ca_timeline_new')
    rows = cursor.fetchall()
    cursor.execute('SELECT id, published_datetime FROM vuln_analyze')
    vulns = cursor.fetchall()
    for vuln in vulns:
        ids = {
            'unknown': [],
            'SQLi': [],
            'Defacement': [],
            'Account Hijacking': [],
            'DDoS': [],
            'Targeted Attack': [],
            'Malware': [],
            'Malicious Code Injection': [],
            'other': [],
        }
        for row in rows:
            if date_diff(row[1], vuln[1]) < int(sys.argv[1]) and date_diff(row[1], vuln[1]) >= 0:
                if row[2] in ids:
                    ids[row[2]].append(row[0])
                else:
                    ids['other'].append(row[0])
        cursor.execute('UPDATE vuln_analyze SET ids=%s WHERE id=%s', (json.dumps(ids), vuln[0]))

def main():
    create_hist()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()
