# -*- coding: utf-8 -*-
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
		self.header = {'User-Agent': 'Mozilla/5.0'}

	def parse(self):
		conn = db.connect(**db_config)
		cursor = conn.cursor()
		with codecs.open(self.content, 'r', encoding='utf-8') as fp:
			content = fp.read()
                        content = content.encode('utf-8')
                        content = json.loads(content)
			for _content in content:
                                name = _content['queries']['request'][0]['searchTerms'].split(' site:')[0]
				for item in _content['items']:
					try:
                                            my_flag = ''
                                            my_count = 0
                                            if 'article:published' in item['pagemap']['metatags'][0]:
                                                    date_orig = item['pagemap']['metatags'][0]['article:published']
                                            elif 'newsarticle' in item['pagemap']:
                                                    if 'datepublished' in item['pagemap']['newsarticle'][0]:
                                                            date_orig = item['pagemap']['newsarticle'][0]['datepublished'] 
                                            else:
                                                    date_orig = ''
                                            url = item['link']
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
                                                    try:
                                                        #ucode.normalize('NFKD', res.encode('utf-8')).encode('ascii','ignore')
                                                        query = "INSERT IGNORE INTO ca_pred (date, content, media, name, url) VALUES ('%s', '%s', '%s', '%s', '%s')" % (date_orig.encode('utf-8'), res.replace("\'", '^'), media.encode('utf-8'), name.encode('utf-8'), url.encode('utf-8'))
                                                        cursor.execute(query) 
                                                    except Exception, e:
                                                            print "inside loop"
                                                            print(e)
					except Exception, e:
					    print(e)
                                            print self.content
		
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
		return res.encode('utf-8') 

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
	for fp in os.listdir(os.getcwd()):
		if fp.startswith('pred_all_'):
                        print fp
			parser = contentParser(fp)
			parser.parse()

if __name__ == '__main__':
	main()
