import mysql.connector as db
import sys
import json
import operator
from itertools import izip

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

def get_vector():
	with open('keywords_' + sys.argv[1] + '.json', 'r') as fp:
		keywords = json.load(fp)
		f_vector = {}
		itr = 0
		for w in keywords:
			f_vector[w] = itr
			itr += 1
	return f_vector

def get_keywords():
	with open('../features/lexicon.dict', 'r') as fp:
		 return json.load(fp)

def set_features():
	keyword_score = get_keywords()
	keywords = get_vector()
	cursor.execute('SELECT max(id) FROM ca_analyze')
	max_id = cursor.fetchone()[0]
	cursor.execute('SELECT min(id) FROM ca_analyze')
	min_id = cursor.fetchone()[0]
	for i in range(min_id, max_id + 1):
		f_vector = [0]*1000
		cursor.execute('SELECT content FROM ca_analyze WHERE id=' + str(i))
		content = cursor.fetchone()
		if content:
			for w in content[0].split(' '):
				if w in keywords:
					f_vector[keywords[w]] += (keyword_score[w] - 0.5)
			cursor.execute('UPDATE ca_analyze SET feature_1000_count_tone_minus=%s WHERE id=%s', (json.dumps(f_vector), str(i)))

def main():
	set_features()
	conn.close()

if __name__ == '__main__':
	main()

