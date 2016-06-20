#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'munkhdorj.bs@gmail.com (B.Munkhdorj)'

import pprint
import json
import datetime
import sys
from googleapiclient.discovery import build
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

cse_info = [
	{
		'apikey':				'AIzaSyBFohvMRhf279vhQAAxqZSLnP73Uo_kYlw',
		'cx':					'017436359385090354107:e9pfmy3vc-s',
		'cnt':				0,
	},
	{
		'apikey':				'AIzaSyBa4DQLPeqfcM9JbD3DNpVEQNZSxC-JaBY',
		'cx':					'011988864748610998685:ujfvr6zf8ri',
		'cnt':				0,
	},
	{
		'apikey':				'AIzaSyB59na9IxtViytGDt0Zo4wncgVkxy00WLg',
		'cx':					'012420782311525976250:tkdzj7fnrag',
		'cnt':				0,
	},
	{
		'apikey':			'AIzaSyBWPE3QFJPjgO0Sus596eW6i4xuW-h1pcE',
		'cx':					'017029776226930534435:5k8qp1lgiug',
		'cnt':				0,
	},
	{
		'apikey':			'AIzaSyDdo1Zmg1sIagujb7Vi4Fzu4OuqGPdb4DE',
		'cx':					'010614785405940198854:twsaffzn2ak',
		'cnt':				0,
	},
	{
		'apikey': 		'AIzaSyCMNQc6W9FnouDZlracOb_XERsWTBY-m3E',
		'cx':					'012435952798677734914:2hovaxtn73c',
		'cnt':				0,
	}
]

def set_date(dt, k):
	tmp = datetime.timedelta(days=k)
	return (dt+tmp).strftime('%Y%m%d') 

def crawl(id, name, service, cse_num):
	fp_all = './pred/pred_all_' + str(id)
	print fp_all
	data = []
	date_st = set_date(datetime.datetime.strptime('2016-1-1', '%Y-%m-%d'), 0)
	date_ed = set_date(datetime.datetime.strptime('2016-6-20', '%Y-%m-%d'), 0)
	for site in sites:
	    print cse_num, cse_info[cse_num]['cnt']
	    if cse_info[cse_num]['cnt'] == 100:
		    if cse_num < len(cse_info) - 1:
			    cse_num += 1
			    service = build('customsearch', 'v1', developerKey=cse_info[cse_num]['apikey'])
			    continue
		    else:
			    return -1
	    else:
		    cse_info[cse_num]['cnt'] += 1
		    res = service.cse().list(
			    q = name + ' ' + sites[site],
			    cx = cse_info[cse_num]['cx'],
			    hl = 'en',
			    siteSearch = 'www.hommee.co',
			    siteSearchFilter = 'e',
			    start = 1,
			    dateRestrict = 'y1',
			    sort = 'date:r:' + date_st + ':' + date_ed,
		    ).execute()
		    if int(res['searchInformation']['totalResults']) > 0:
                        data.append(res)
	with open(fp_all, 'w') as fp:
		fp.write(json.dumps(data))
	
	return 1

def main():
	cse_num = int(sys.argv[1])
	service = build("customsearch", "v1", developerKey=cse_info[cse_num]['apikey'])
	conn = db.connect(**db_config)
	cursor = conn.cursor()
	query = "SELECT * FROM top_targets"
	cursor.execute(query)
	result = cursor.fetchall()
	for row in result:
		last_id = row[0]
		ret = crawl(row[0], row[1], service, cse_num)
		if ret == -1:
	            break
	query = "UPDATE log_tt SET last_id=%s WHERE id=1" % str(last_id)
	cursor.execute(query)
	conn.close()

if __name__ == '__main__':
  main()
