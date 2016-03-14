import mysql.connector as db

db_config = {
		'user': 'root',
		'password': 'root',
		'host': '127.0.0.1',
		'port': 8889,
		'database': 'cnl',
		'raise_on_warnings': False,
		'autocommit': True,
	}

conn = db.connect(**db_config)
cursor = conn.cursor()

query = ("INSERT INTO ca_timeline_new "
		 "(date, author, target, target_desc, attack_desc, attack_type, target_category, attack_category, country) "
		 #"VALUES (%(date)s, %(author)s, %(target)s, %(target_desc)s, %(attack_desc)s, %(attack_type)s, %(target_category)s, %(attack_category)s, %(country)s) ") 
		 "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ") 

with open('/Users/mugi/CNL/cyber-attack-info/jan_feb.csv', 'r') as fp:
	for line in fp:
		row = line.rstrip().split(',')
		#print row
		cursor.execute(query, row)		

conn.close()
