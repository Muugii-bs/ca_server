import os
os.environ['http_proxy']=''
import urllib2, httplib
import unicodedata as ucode
import gzip
import StringIO
import pprint
import json 
from bs4 import BeautifulSoup as bs
from cookielib import CookieJar
import sys
import mysql.connector as db
import re
import time
	
db_config = {
		'user':								'root',
		'password':						'root',
		'host':								'127.0.0.1',
		'port':								'3306',
		'database':						'cnl',
		'raise_on_warnings': 	False,
		'autocommit': 				True,
	}


class contentParser:
	
	def __init__(self, ifile):
		self.content = ifile
		name = ifile.split('_')
		self.content_id = name[0]
		self.content_type = name[1]
		self.content_date = name[2]
		self.header = {'User-Agent': 'Mozilla/5.0'}

	def parse(self):
		conn = db.connect(**db_config)
		cursor = conn.cursor()
		with open(self.content, 'r') as fp:
			content = json.load(fp)
			print json.dumps(content, indent=4, sort_keys=True)
			for item in content:
                                time.sleep(2)
				attack_type = item['attack_type']
				attack_category = item['attack_category']
				author = item['author']
				country = item['country']
				date = item['date']
				target = item['target']
				target_category = item['target_category']
				my_count = 0
				for url in item['link']:
					res = ''
					if 'video' in url:
						continue
					elif 'image' in url:
						continue
					elif 'www.pravdareport.com' in url:
						res = self.parse_pravda(url)
						media = 'pravda'
					elif 'www.rt.com' in url:
						res = self.parse_rt(url)
						media = 'rt'
					elif 'www.washingtonpost.com' in url:
						res = self.parse_wp(url)
						media = 'washingtonpost'
					elif 'www.nytimes.com' in url:
						res = self.parse_nyt(url)
						media = 'nytimes'
					elif 'www.japantimes.co.jp' in url:
						res = self.parse_jpt(url)
						media = 'japantimes'
					elif 'www.nbcnews.com' in url:
						res = self.parse_nbc(url)
						media = 'nbcnews'
					elif 'www.theguardian.com' in url:
						res = self.parse_guardian(url)
						media = 'theguardian'
					elif 'www.bbc.com' in url:
						res = self.parse_bbc(url)
						media = 'bbc'
					elif 'news.yahoo.com' in url:
						res = self.parse_yahoo(url)
						media = 'yahoo'
					elif 'www.foxnews.com' in url:
						res = self.parse_fox(url)
						media = 'foxnews'
					elif 'www3.nhk.or.jp' in url:
						res = self.parse_nhk(url)
						media = 'nhk'
					elif 'www.chinadaily.com.cn' in url:
						res = self.parse_cndaily(url)
						media = 'chinadaily'
					elif 'www.aljazeera.com' in url:
						res = self.parse_alj(url)
						media = 'aljazeera'
					elif 'www.moscowtimes.com' in url:
						res = self.parse_moscowt(url)
						media = 'moscowtimes'
					elif 'www.shanghaidaily.com' in url:
						res = self.parse_shanghaid(url)
						media = 'shanghaidaily'
					my_count += 1
					if res:
						ucode.normalize('NFKD', unicode(res)).encode('ascii','ignore')
                                                res = unicode(re.sub('[^\w\s-]', '', res).strip().lower())
                                                res = re.sub('[-\s]+', ' ', res)
						print url
						print res
						query = ("INSERT INTO ca_analyze "
										"(attack_id, target, date, author, attack_type, attack_category, target_category, country, flag, count, content, media, url) "
										    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
										    "ON DUPLICATE KEY UPDATE attack_id=%s, target=%s, date=%s, author=%s, attack_type=%s, attack_category=%s, target_category=%s, country=%s, "
										    "flag=%s, count=%s, content=%s, media=%s, url=%s"
										    )
                                                cursor.execute(query, (self.content_id, target, self.content_date, author, attack_type, attack_category, target_category, country, self.content_type, my_count, res, media, url, self.content_id, target, self.content_date, author, attack_type, attack_category, target_category, country, self.content_type, my_count, res, media, url)) 
	
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
			article = article.find_all("p")
			for p in article:
				res += p.get_text()
				res += ' '
		return res 

	def parse_rt(self, url):
		res = ''
		text = self.parse_init(url) 
		res = text.body.find('div', attrs={'class': 'article__summary'}).get_text()
		article = text.body.find('div', attrs={'class': 'article__text'})
		if article:
			article = article.find_all("p")
			for p in article:
				res += p.get_text()
				res += ' '
		return res 

	def parse_yahoo(self, url):
		res = ''
		text = self.parse_init(url) 
		article = text.body.find('div', attrs={'class': 'yom-art-content'})
		if article:
			article = article.find_all("p")
			for p in article:
				res += p.get_text()
				res += ' '
		return res 

	def parse_nyt(self, url):
		res = ''
		text = self.parse_init(url) 
		article = text.body.find('div', attrs={'id': 'story-body'})
		if article:
			article = article.find_all("p")
			for p in article:
				res += p.get_text()
				res += ' '
		return res 

	def parse_wp(self, url):
		res = ''
		text = self.parse_init(url) 
		article = text.body.find('article', attrs={'itemprop': 'articleBody'})
		if article:
			article = article.find_all("p")
			for p in article:
				res += p.get_text()
				res += ' '
		return res 

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
		return res

	def parse_jpt(self, url):
		res = ''
		text = self.parse_init(url) 
		article = text.body.find('div', attrs={'id': 'jtarticle'})
		if article:
			article = article.find_all("p")
			for p in article:
				res += p.get_text()
				res += ' '
		return res 

	def parse_nbc(self, url):
		res = ''
		text = self.parse_init(url) 
		article = text.body.find('div', attrs={'itemprop': 'articleBody'})
		if article:
			article = article.find_all("p")
			for p in article:
				res += p.get_text()
				res += ' '
		return res 

	def parse_bbc(self, url):
		res = ''
		text = self.parse_init(url) 
		article = text.body.find('div', attrs={'property': 'articleBody'})
		if article:
			article = article.find_all("p")
			for p in article:
				res += p.get_text()
				res += ' '
		return res 

	def parse_fox(self, url):
		res = ''
		text = self.parse_init_off(url) 
		article = text.body.find('div', attrs={'itemprop': 'articleBody'})
		if article:
			article = article.find_all("p")
			for p in article:
				res += p.get_text()
				res += ' '
		return res 

	def parse_nhk(self, url):
		res = ''
		text = self.parse_init(url) 
		article = text.body.find('div', attrs={'class': 'content'})
		if article:
			article = article.find_all("p")
			for p in article:
				res += p.get_text()
				res += ' '
		return res 

	def parse_cndaily(self, url):
		res = ''
		text = self.parse_init_off(url) 
		article = text.find('div', attrs={'id': 'Content'})
		if article:
			article = article.find_all("p")
			for p in article:
				res += p.get_text()
				res += ' '
		return res 

	def parse_alj(self, url):
		res = ''
		text = self.parse_init_off(url) 
		article = text.body.find('div', attrs={'id': 'article-body'})
		if article:
			article = article.find_all("p")
			for p in article:
				res += p.get_text()
				res += ' '
		return res 

	def parse_moscowt(self, url):
		res = ''
		text = self.parse_init_off(url) 
		article = text.body.find('div', attrs={'class': 'article_text'})
		if article:
			article = article.find_all("p")
			for p in article:
				res += p.get_text()
				res += ' '
		return res 

	def parse_guardian(self, url):
		res = ''
		text = self.parse_init_off(url) 
		article = text.body.find('div', attrs={'itemprop': 'articleBody'})
		if article:
			article = article.find_all("p")
			for p in article:
				res += p.get_text()
				res += ' '
		return res 

def main():
    parser = contentParser(sys.argv[1])
    parser.parse()


if __name__ == '__main__':
    main()
