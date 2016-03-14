import urllib2, httplib
import unicodedata as ucode
import codecs
import datetime
import gzip
import StringIO
import pprint
import json 
from bs4 import BeautifulSoup as bs
from cookielib import CookieJar
import sys
import mysql.connector as db
import os
import re
#{{{1	
db_config = {
		'user':								'root',
		'password':						'root',
		'host':								'127.0.0.1',
		'port':								'8889',
		'database':						'cnl',
		'raise_on_warnings': 	False,
		'autocommit': 				True,
	}

columns = {
		'id':					0,
		'date':					1,
		'author':				2,
		'target':				3,
		'attack_type':			4,
		'attack_category':			5,
		'target_category':		6,
		'country':		7,
		'attack_id':				8,
		'flag':			9,
		'count':	10,
		'content': 11,
		'media': 12,
		'url': 13,
		'senti': 14,
		'f1': 15,
		'f2': 16,
		'f3': 17,
		'f4': 18,
		'date_orig': 19,
		'new_flag': 20
}

months = {
		'Jan': '01',
		'Feb': '02',
		'Mar': '03',
		'Apr': '04',
		'May': '05',
		'Jun': '06',
		'Jul': '07',
		'Aug': '08',
		'Sep': '09',
		'Oct': '10',
		'Nov': '11',
		'Dec': '12'
}
#}}}1
class contentParser:
	
	def __init__(self):
		self.header = {'User-Agent': 'Mozilla/5.0'}

	def parse(self):
		conn = db.connect(**db_config)
		cursor = conn.cursor()
		#cursor.execute('SELECT * FROM ca_analyze WHERE date_orig IS NULL OR date_orig = "0000-00-00"')
		#for row in cursor:
		#try:
		#url = row[columns['url']]
		url = sys.argv[1]
		if 'video' in url:
					#continue
					print "video"
		elif 'image' in url:
					#continue
					print "image"
		elif 'www.pravdareport.com' in url:
					res = self.parse_pravda(url)
		elif 'www.rt.com' in url:
					res = self.parse_rt(url)
		elif 'www.washingtonpost.com' in url:
					res = self.parse_wp(url)
		elif 'www.nytimes.com' in url:
					res = self.parse_nyt(url)
		elif 'www.japantimes.co.jp' in url:
					res = self.parse_jpt(url)
		elif 'www.nbcnews.com' in url:
					res = self.parse_nbc(url)
		elif 'www.theguardian.com' in url:
					res = self.parse_guardian(url)
		elif 'www.bbc.com' in url:
					res = self.parse_bbc(url)
		elif 'news.yahoo.com' in url:
					res = self.parse_yahoo(url)
		elif 'www.foxnews.com' in url:
					res = self.parse_fox(url)
		elif 'www3.nhk.or.jp' in url:
					res = self.parse_nhk(url)
		elif 'www.chinadaily.com.cn' in url:
					res = self.parse_cndaily(url)
		elif 'www.aljazeera.com' in url:
					res = self.parse_alj(url)
		elif 'www.moscowtimes.com' in url:
					res = self.parse_moscowt(url)
		elif 'www.shanghaidaily.com' in url:
					res = self.parse_shanghaid(url)
		#if res:
			#try:
		query = 'UPDATE ca_analyze SET url=%s WHERE id=%s'		
		#cursor.execute(query, (res, row[columns['id']]) 
		print res
		
		conn.close()

	def parse_init(self, url):
		cj = CookieJar()
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 5.1; rv:10.0.1) Gecko/20100101 Firefox/10.0.1')]
		html = opener.open(url)
		return bs(html.read(), 'html.parser')

	def parse_init_off(self, url):
		req = urllib2.Request(url, headers=self.header)
		html = urllib2.urlopen(req)
		return bs(html.read(), 'html.parser')

	def parse_pravda(self, url):
		res = ''
		text = self.parse_init(url) 
		article = text.body.find('div', attrs={'id': 'article'})
		if article:
			_date = article.find('div', attrs={'class': 'date'}).get_text()
			_date = re.search("\d\d\.\d\d\.\d\d\d\d", _date).group()
			_date = _date.split('.')
			res = _date[2] + '-' + _date[1] + '-' + _date[0]
		return res.encode('utf-8') 

	def parse_rt(self, url):
		res = ''
		text = self.parse_init(url) 
		_date = text.body.find('div', attrs={'class': 'article__date'})
		_date = _date.find('time', attrs={'class': 'date_article-header'}).get_text()
		if _date:
			_date = re.search("\d{1,2}\s[A-z][a-z][a-z]\,\s\d{4}", _date).group()
			_date = _date.split(' ')
			res = _date[2] + '-' + months[_date[1].replace(',', '')] + '-' + _date[0]
		return res.encode('utf-8') 

	def parse_yahoo(self, url):
		res = ''
		text = self.parse_init(url) 
		article = text.body.find('div', attrs={'class': 'yom-art-content'})
		if article:
			article = article.find_all("p")
			for p in article:
				res += p.get_text()
				res += ' '
		return res.encode('utf-8') 

	def parse_nyt(self, url):
		res = ''
		text = self.parse_init(url) 
		article = text.body.find('div', attrs={'id': 'story-body'})
		if article:
			article = article.find_all("p")
			for p in article:
				res += p.get_text()
				res += ' '
		return res.encode('utf-8') 

	def parse_wp(self, url):
		res = ''
		text = self.parse_init(url) 
		article = text.body.find('article', attrs={'itemprop': 'articleBody'})
		if article:
			article = article.find_all("p")
			for p in article:
				res += p.get_text()
				res += ' '
		return res.encode('utf-8') 

	def parse_shanghaid(self, url):
		res = ''
		httplib.HTTPConnection.debuglevel = 1
		request = urllib2.Request(url)
		request.add_header('Accept-encoding', 'gzip') 
		opener = urllib2.build_opener()
		html = opener.open(request)
		data = html.read()
		data = StringIO.StringIO(data)
		gzipper = gzip.GzipFile(fileobj=data)
		text = gzipper.read()
		text = bs(text, 'html.parser')
		article = text.find('div', attrs={'class': 'detail_content'})
		if article:
			article = article.find_all("p")
			for p in article:
				res += p.get_text()
				res += ' '
		return res.encode('utf-8')

	def parse_jpt(self, url):
		res = ''
		text = self.parse_init(url) 
		article = text.body.find('div', attrs={'id': 'jtarticle'})
		if article:
			article = article.find_all("p")
			for p in article:
				res += p.get_text()
				res += ' '
		return res.encode('utf-8') 

	def parse_nbc(self, url):
		res = ''
		text = self.parse_init(url) 
		article = text.body.find('div', attrs={'itemprop': 'articleBody'})
		if article:
			article = article.find_all("p")
			for p in article:
				res += p.get_text()
				res += ' '
		return res.encode('utf-8') 

	def parse_bbc(self, url):
		res = ''
		text = self.parse_init(url) 
		article = text.body.find('div', attrs={'property': 'articleBody'})
		if article:
			article = article.find_all("p")
			for p in article:
				res += p.get_text()
				res += ' '
		return res.encode('utf-8') 

	def parse_fox(self, url):
		res = ''
		text = self.parse_init_off(url) 
		article = text.body.find('div', attrs={'itemprop': 'articleBody'})
		if article:
			article = article.find_all("p")
			for p in article:
				res += p.get_text()
				res += ' '
		return res.encode('utf-8') 

	def parse_nhk(self, url):
		res = ''
		text = self.parse_init(url) 
		article = text.body.find('div', attrs={'class': 'content'})
		if article:
			article = article.find_all("p")
			for p in article:
				res += p.get_text()
				res += ' '
		return res.encode('utf-8') 

	def parse_cndaily(self, url):
		res = ''
		text = self.parse_init_off(url) 
		article = text.find('div', attrs={'id': 'Content'})
		if article:
			article = article.find_all("p")
			for p in article:
				res += p.get_text()
				res += ' '
		return res.encode('utf-8') 

	def parse_alj(self, url):
		res = ''
		text = self.parse_init_off(url) 
		article = text.body.find('div', attrs={'id': 'article-body'})
		if article:
			article = article.find_all("p")
			for p in article:
				res += p.get_text()
				res += ' '
		return res.encode('utf-8') 

	def parse_moscowt(self, url):
		res = ''
		text = self.parse_init_off(url) 
		article = text.body.find('div', attrs={'class': 'article_text'})
		if article:
			article = article.find_all("p")
			for p in article:
				res += p.get_text()
				res += ' '
		return res.encode('utf-8') 

	def parse_guardian(self, url):
		res = ''
		text = self.parse_init_off(url) 
		article = text.body.find('div', attrs={'itemprop': 'articleBody'})
		if article:
			article = article.find_all("p")
			for p in article:
				res += p.get_text()
				res += ' '
		return res.encode('utf-8') 

def main():
		parser = contentParser()
		parser.parse()

if __name__ == '__main__':
	main()
