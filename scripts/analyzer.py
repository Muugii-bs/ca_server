from nltk.tokenize import word_tokenize as w_t
from nltk.corpus import stopwords
import mysql.connector as db
from pprint import pprint
import string
import nltk
import sys
import re

db_config = {
		'user':								'root',
		'password':						'root',
		'host':								'127.0.0.1',
		'port':								'8889',
		'database':						'cnl',
		'raise_on_warnings': 	False,
		'autocommit': 				True,
}

class Analyzer:

	def __init__(self, text):
		self.content = text
		self.sents = []
		self.tokens = []
		self.sents = [w_t(report) for report in self.content]
		
	def clean(self):
		regex = re.compile('[%s]' % re.escape(string.punctuation))
		for sent in self.sents:
			tokens = []
			for words in sent:
				token = regex.sub(u'', words)
				if not token == u'':
					tokens.append(token)
			self.tokens.append(tokens)	

def main():
	nltk.download('punkt')
	conn = db.connect(**db_config)
	cursor = conn.cursor()
	query  = "SELECT content FROM ca_analyze WHERE id=" + sys.argv[1]
	cursor.execute(query)
	analyzer = Analyzer(cursor.fetchone())
	analyzer.clean()
	for block in  analyzer.tokens:
		for term in block:
			print term

if __name__ == '__main__':
	main()

