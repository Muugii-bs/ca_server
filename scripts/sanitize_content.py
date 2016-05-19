import mysql.connector as db
import json
import re

db_config = {
		'host':				'127.0.0.1',
		'user':				'root',
		'password':		'root',
		'port':				3306,
		'database':		'cnl',
		'autocommit':	True,
	}

conn = db.connect(**db_config)
cursor = conn.cursor()

def sanitize():
    cursor.execute('SELECT max(id) FROM ca_analyze')
    max_id = cursor.fetchone()
    for i in range(1, max_id[0]+1):
	cursor.execute('SELECT content FROM ca_analyze WHERE id=' + str(i))
	article = cursor.fetchone()
	if article is not None:
            article = article[0].strip('\n')
            article = unicode(re.sub('[^\w\s-]', '', article).lower())
            article = re.sub('[-\s]+', ' ', article)
            sql = "UPDATE ca_analyze SET content=%s WHERE id=%s"
            cursor.execute(sql, (article, str(i)))

def main():
    sanitize()

if __name__ == '__main__':
    main()
