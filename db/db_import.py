import mysql.connector as db
from datetime import datetime
import sys

db_config = {
		'user': 'root',
		'password': 'root',
		'host': '127.0.0.1',
		'port': 3306,
		'database': 'cnl',
		'raise_on_warnings': False,
		'autocommit': True,
	}

conn = db.connect(**db_config)
cursor = conn.cursor()

query = ("INSERT INTO ca_timeline_new "
		 "(date, author, target_desc, attack_type, target_category, attack_category, country) "
		 #"VALUES (%(date)s, %(author)s, %(target)s, %(target_desc)s, %(attack_desc)s, %(attack_type)s, %(target_category)s, %(attack_category)s, %(country)s) ") 
		 "VALUES (%s, %s, %s, %s, %s, %s, %s) ") 

with open(sys.argv[1], 'r') as fp:
	for line in fp:
		row = line.rstrip().split('\t')
                row[0] = datetime.strftime(datetime.strptime(row[0], '%d/%m/%Y'), '%Y-%m-%d')
                print row
		cursor.execute(query, row)		

conn.close()
