#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'munkhdorj.bs@gmail.com (B.Munkhdorj)'

import pprint
import json
import datetime
import sys
from googleapiclient.discovery import build
import mysql.connector as db
	
db_config = {
		'user':								'root',
		'password':						'root',
		'host':								'127.0.0.1',
		'port':								'8889',
		'database':						'cnl',
		'raise_on_warnings': 	False,
		'autocommit': 				True,
	}

sites = {
		'yahoo':							'site:news.yahoo.com',
		'guardians':					'site:www.theguardian.com',
		'nytimes':						'site:www.nytimes.com',
		'foxnews':						'site:www.foxnews.com',
		'washingtonpost':			'site:www.washingtonpost.com',
		'bbc':								'site:www.bbc.com/news/',
		'nbcnews':						'site:www.nbcnews.com',
		'aljazeera':					'site:www.aljazeera.com',
		'chinadaily':					'site:www.chinadaily.com.cn',
		'shanghaidaily': 			'site:www.shanghaidaily.com',
		'moscowtimes': 				'site:www.themoscowtimes.com',
		'pravda': 						'site:www.pravdareport.com',
		'rt': 								'site:www.rt.com/news/',
		'japantimes': 				'site:www.japantimes.co.jp/news/',
		'nhknews':						'site:www3.nhk.or.jp/nhkworld/english/news/',
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

cse_info = [
	{
		'apikey':				'AIzaSyBFohvMRhf279vhQAAxqZSLnP73Uo_kYlw',
		'cx':					'017436359385090354107:e9pfmy3vc-s',
	},
	{
		'apikey':				'AIzaSyBa4DQLPeqfcM9JbD3DNpVEQNZSxC-JaBY',
		'cx':					'011988864748610998685:ujfvr6zf8ri',
	},
	{
		'apikey':				'AIzaSyB59na9IxtViytGDt0Zo4wncgVkxy00WLg',
		'cx':					'012420782311525976250:tkdzj7fnrag',
	},
	{
		'apikey':			'AIzaSyBWPE3QFJPjgO0Sus596eW6i4xuW-h1pcE',
		'cx':					'017029776226930534435:5k8qp1lgiug'
	},
	{
		'apikey':			'AIzaSyDdo1Zmg1sIagujb7Vi4Fzu4OuqGPdb4DE',
		'cx':					'010614785405940198854:twsaffzn2ak',
	},
	{
		'apikey': 		'AIzaSyCMNQc6W9FnouDZlracOb_XERsWTBY-m3E',
		'cx':					'012435952798677734914:2hovaxtn73c'
	}
]

my_apikey = cse_info[int(sys.argv[1])]['apikey']
my_cx = cse_info[int(sys.argv[1])]['cx']
service = build("customsearch", "v1", developerKey=my_apikey)

def set_date(dt, k):
	tmp = datetime.timedelta(days=k)
	return (dt+tmp).strftime('%Y%m%d') 

def crawl(row, flag):
	data = []
	if flag == 'on':
		date_st = set_date(row[1], -7)
		date_ed = set_date(row[1], 0)
	elif flag == 'off':
		date_st = set_date(row[1], -30)
		date_ed = set_date(row[1], -8)
	for target in row[columns['target_desc']].split(';'):
		block = {}
		block['target'] = target 
		block['date'] = row[columns['date']].strftime('%Y-%m-%d')
		block['author'] = row[columns['author']]
		block['attack_type'] = row[columns['attack_type']]
		block['attack_category'] = row[columns['attack_category']]
		block['target_category'] = row[columns['target_category']]
		block['country'] = row[columns['country']]
		block['link'] = []
		for site in sites:
			res = service.cse().list(
				q = target + ' ' + sites[site],
				cx = my_cx,
				hl = 'en',
				siteSearch = 'www.hommee.co',
				siteSearchFilter = 'e',
				start = 1,
				dateRestrict = 'y1',
				sort = 'date:r:' + date_st + ':' + date_ed,
			).execute()
			if int(res['searchInformation']['totalResults']) > 0:
				print json.dumps(res)
				for item in res['items']:
					block['link'].append(item['link'])
		data.append(block)
	return json.dumps(data)

def main():
	conn = db.connect(**db_config)
	cursor = conn.cursor()
	query = "SELECT * from ca_timeline_new WHERE id=" + sys.argv[2]
	cursor.execute(query)
	result = cursor.fetchall()
	for row in result:
		fp = str(row[columns['id']]) + '_on_' + datetime.datetime.strftime(row[columns['date']], '%Y-%m-%d') + '.txt'
		with open(fp, 'w') as f:
			f.write(crawl(row, 'on'))
		fp = str(row[columns['id']]) + '_off_' + datetime.datetime.strftime(row[columns['date']], '%Y-%m-%d') + '.txt'
		with open(fp, 'w') as f:
			f.write(crawl(row, 'off'))
			
	conn.close()

if __name__ == '__main__':
  main()
