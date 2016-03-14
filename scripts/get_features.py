import mysql.connector as db
import sys
import json
import operator
from itertools import izip

FILE_LEXICON = 'lexicon.dict'

db_config = {
		'host':			'127.0.0.1',
		'port':			3306,
		'user':			'root',
		'password':	'root',
		'database':	'cnl',
		'autocommit': True,
}
conn = db.connect(**db_config)
cursor = conn.cursor()

def get_lexicon():
	with open(FILE_LEXICON, 'r') as fp:
		lexicon = json.load(fp)
	return lexicon

def get_features():
	lexicon = get_lexicon()	
	features = {}
	keywords = {}
	query = ('SELECT id FROM ca_analyze INNER JOIN '
					'(SELECT DISTINCT url FROM ca_analyze GROUP BY id) '
					'AS t1 ON ca_analyze.url=t1.url')
	cursor.execute(query)
	ids = cursor.fetchall()
	for i in ids:
		cursor.execute('SELECT content FROM ca_analyze WHERE id=' + str(i[0]))
		content = cursor.fetchone()
		if content:
			text = content[0].strip().split(' ')
			for w in text:
				if w in lexicon:
					if w in features:
						features[w] += 1
					else:
						features[w] = 0
				else:
					continue
	features = sorted(features.items(), key=operator.itemgetter(1), reverse=True)
	features = features[:int(sys.argv[1])]
	for pair in features:
		keywords[pair[0]] = pair[1] 
	print json.dumps(keywords)

def main():
	get_features()
	conn.close()

if __name__ == '__main__':
	main()

