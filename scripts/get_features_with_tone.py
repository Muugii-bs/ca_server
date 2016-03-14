import mysql.connector as db
import sys
import json
import operator
from itertools import izip

FILE_LEXICON = '../features/lexicon.dict'
VECTOR_DIM = int(sys.argv[1]) / 2

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

def get_lexicon(flag):
	lexicon = []
	with open(FILE_LEXICON, 'r') as fp:
		tmp = json.load(fp)
		for k in tmp:
			if tmp[k] == flag:
				lexicon.append(k)
	return lexicon

def get_hits(lexicon, flag):
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
	features = features[:VECTOR_DIM]
	for pair in features:
		keywords[pair[0]] = flag 
	return keywords

def get_features():
	lexicon_neg = get_lexicon(-1)	
	lexicon_pos = get_lexicon(1)
	neg = get_hits(lexicon_neg, -1)
	pos = get_hits(lexicon_pos, 1)
	return dict(neg, **pos)
			
def main():
	print json.dumps(get_features())
	conn.close()

if __name__ == '__main__':
	main()

