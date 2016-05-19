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

columns = {
		'id':					0,
		'date':					1,
		'author':				2,
		'target':				3,
		'attack_desc':			4,
		'attack_type':			5,
		'attack_category':		6,
		'target_category':		7,
		'country':				8,
		'target_desc':			9,
}

class contentParser:
	
	def __init__(self, ifile):
		self.content = ifile
		name = ifile.split('_')
		self.content_id = name[1]
                print name[1]
		self.header = {'User-Agent': 'Mozilla/5.0'}

	def parse(self):
                print self.content_id
		conn = db.connect(**db_config)
		cursor = conn.cursor()
		with codecs.open(self.content, 'r', encoding='utf-8') as fp:
			content = fp.read()
                        content = content.encode('utf-8')
                        content = json.loads(content)
			cursor.execute('SELECT * FROM ca_timeline_new WHERE id=%s',(self.content_id,))
			tmp = cursor.fetchone()
			attack_type = tmp[columns['attack_type']]
			attack_category = tmp[columns['attack_category']]
			author = tmp[columns['author']]
			country = tmp[columns['country']]
			my_date = tmp[columns['date']]
			target = tmp[columns['target_desc']]
			target_category = tmp[columns['target_category']]
			#print 'id', self.content_id, 'target', target, 'date', my_date, 'author', author, 'attack_type', attack_type, 'attack_category', attack_category, 'target_category', target_category, 'country', country
			#print json.dumps(content, indent=4, sort_keys=True)
			for _content in content:
				for item in _content['items']:
					try:
                                            date_orig = ''
                                            my_flag = ''
                                            my_count = 0
                                            if 'article:published' in item['pagemap']['metatags'][0]:
                                                    date_orig = item['pagemap']['metatags'][0]['article:published']
                                            elif 'newsarticle' in item['pagemap']:
                                                    if 'datepublished' in item['pagemap']['newsarticle'][0]:
                                                            date_orig = item['pagemap']['newsarticle'][0]['datepublished'] 
                                            else:
                                                    date_orig = ''
                                            if date_orig:
                                                    tmp = datetime.timedelta(days=-7)
                                                    if (my_date + tmp).strftime('%Y-%m-%d') < date_orig:
                                                            my_flag = 'on'
                                                    else:
                                                            my_flag = 'off'
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
                                            #print url, 'date_orig', date_orig, 'my_flag', my_flag, 'media', media
                                            if res:
                                                    try:
                                                        #ucode.normalize('NFKD', res).encode('ascii','ignore')
                                                        #print url
                                                        #print self.content_id
                                                        #print res
                                                        query = ("INSERT INTO ca_analyze "
                                                            "(attack_id, target, date, author, attack_type, attack_category, target_category, country, flag, count, content, media, url, date_orig, new_flag) "
                                                            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 1) "
                                                            "ON DUPLICATE KEY UPDATE attack_id=%s, target=%s, date=%s, author=%s, attack_type=%s, attack_category=%s, target_category=%s, country=%s, "
                                                            "flag=%s, count=%s, content=%s, media=%s, url=%s, date_orig=%s, new_flag=1"
                                                            )
                                                        values = (self.content_id, target, my_date, author, attack_type, attack_category, target_category, country, my_flag, my_count, res, media, url, date_orig, self.content_id, target, my_date, author, attack_type, attack_category, target_category, country, my_flag, my_count, res, media, url, date_orig)
                                                        cursor.execute(query, values) 
                                                    except Exception, e:
                                                            print self.content_id
                                                            print(e)
					except Exception, e:
                                            print self.content_id
					    print(e)
		
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
		if fp.startswith('all_'):
			parser = contentParser(fp)
			parser.parse()

if __name__ == '__main__':
	main()
