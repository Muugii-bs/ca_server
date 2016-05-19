#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'munkhdorj.bs@gmail.com (B.Munkhdorj)'

from pprint import pprint
import json
from datetime import datetime
import sys
from googleapiclient.discovery import build
import mysql.connector as db
	
db_config = {
		'user':								'root',
		'password':						'root',
		'host':								'127.0.0.1',
		'port':								'3306',
		'database':						'cnl',
		'raise_on_warnings': 	False,
		'autocommit': 				True,
	}

def set_date(cursor, cursor1, k):
    cursor.execute('SELECT date, date_orig, id FROM ca_analyze WHERE new_flag=1')
    res = cursor.fetchall()
    for row in res:
        if row[0] is not None and row[1] is not None:
            diff = (row[0] - row[1]).days
            print row[2],row[0],row[1],diff
            if int(diff) <= k and diff > 0:
                print " on ", row[2]
                cursor1.execute('UPDATE ca_analyze SET flag="on" WHERE id=%d' % (row[2]))
            elif diff > k:
                print " off ", row[2]
                cursor1.execute('UPDATE ca_analyze SET flag="off" WHERE id=%d' % (row[2]))
            else:
                cursor1.execute('UPDATE ca_analyze SET flag="out" WHERE id=%d' % (row[2]))
        
def main():
	conn = db.connect(**db_config)
        conn1 = db.connect(**db_config)
	cursor = conn.cursor()
	cursor1 = conn.cursor()
        set_date(cursor, cursor1, int(sys.argv[1]))			
	conn.close()

if __name__ == '__main__':
  main()
