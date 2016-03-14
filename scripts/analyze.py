import mysql.connector as db
import json

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
FILE_LEXICON = 'lexicon.dict'

def get_lexicon():
	with open(FILE_LEXICON, 'r') as fp:
		lexicon = json.load(fp)
	return lexicon

def get_senti(lexicon, text):
	senti = {}
	senti['score'] = 0.0
	senti['count'] = 0
	for e in text.split(" "):
		if e in lexicon:
			senti['score'] += float(lexicon[e])
			senti['count'] += 1
	return senti

def senti_analyze():
	lexicon = get_lexicon()
	cursor.execute('SELECT max(id) FROM ca_analyze')
	max_id = cursor.fetchone()
	for i in range(1, max_id[0]+1):
		cursor.execute('SELECT content FROM ca_analyze WHERE id=' + str(i))
		article = cursor.fetchone()
		if article:
			senti = get_senti(lexicon, article[0])
                        if senti['count']:
                            print i
                            print senti
                            cursor.execute("UPDATE ca_analyze SET senti='" + str(senti['score']/senti['count']) + "'  WHERE id='" + str(i) + "'")

def main():
	senti_analyze()

if __name__ == '__main__':
	main()
