import sys
import json
import operator
from itertools import izip
import mysql.connector as db
from datetime import datetime
from pprint import pprint

FILE_LEXICON = 'lexicon.dict'

'''
RESULT = {
    'attack_type': {
        'sqli': {
            'count': [0] * 61,
            'senti': [0] * 61,
            'senti_sum': [0] * 61,
        }
    }
    'attack_category': {
        'sqli': {
            'count': [0] * 61,
            'senti': [0] * 61,
            'senti_sum': [0] * 61,
        }
    }
    'target_category': {
        'sqli': {
            'count': [0] * 61,
            'senti': [0] * 61,
            'senti_sum': [0] * 61,
        }
    }
}
'''

db_config = {
    'host':	    '127.0.0.1',
    'port':	    3306,
    'user':	    'root',
    'password':	    'root',
    'database':	    'cnl',
    'autocommit':   True,
}

RESULT = {
    'attack_type': {},
    'attack_category': {},
    'target_category': {},
    'all': {
        'count': [0] * 61,
        'senti': [0.0] * 61,
        'senti_sum': [0] * 61,
    }
} 

FOLDER = './hist_result'
FOLDER_COUNT = FOLDER + '/%s/count/'
FOLDER_SENTI = FOLDER + '/%s/senti/'

conn = db.connect(**db_config)
cursor = conn.cursor()

def date_diff(attack_date, publish_date):
    res = (attack_date - publish_date).days
    if res < 0 or res > 60:
        return 60
    else:
        return int(res)

def create_hist():
    cursor.execute('SELECT MIN(id), MAX(id) FROM ca_analyze')
    min_id, max_id = cursor.fetchone()
    for i in range(min_id, max_id + 1):
        cursor.execute('SELECT attack_type, attack_category, target_category, date, date_orig, senti \
            FROM ca_analyze WHERE new_flag=1 AND date_orig <> "0000-00-00" AND senti IS NOT NULL AND id = %d' % (i))
        row = cursor.fetchone()
        if not row == None:
            if not (row[0] == None and row[1] == None and row[2] == None and row[3] == None and row[4] == None and row[5] == None):
               print i
               a_type = row[0].replace(' ', '').lower() 
               a_cat = row[1].replace(' ', '').lower() 
               t_cat = row[2].replace(' ', '').lower() 
               put_statics('all', a_type, row[3], row[4], row[5])
               put_statics('attack_type', a_type, row[3], row[4], row[5])
               put_statics('attack_category', a_cat, row[3], row[4], row[5])
               put_statics('target_category', t_cat, row[3], row[4], row[5])

def write_result():
    for k, v in RESULT.iteritems():
        if k == 'all':
            for i in range(0, 61):
                with open(FOLDER_COUNT % k + 'result', 'a') as fp1:
                    fp1.write(str(i) + '\t' + str(v['count'][i]) + '\n') 
                if not v['senti_sum'][i] == 0:
                    with open(FOLDER_SENTI % k + 'result', 'a') as fp2:
                        fp2.write(str(i) + '\t' + str(v['senti'][i] / v['senti_sum'][i]) + '\n')
                else:
                    with open(FOLDER_SENTI % k + 'result', 'a') as fp2:
                        fp2.write(str(i) + '\t' + str(v['senti'][i]) + '\n')
        else:
            for k1, v1 in v.iteritems():
                for i in range(0, 61):
                    with open(FOLDER_COUNT % k + k1, 'a') as fp1:
                        fp1.write(str(i) + '\t' + str(v1['count'][i]) + '\n') 
                    if not v1['senti_sum'][i] == 0:
                        with open(FOLDER_SENTI % k + k1, 'a') as fp2:
                            fp2.write(str(i) + '\t' + str(v1['senti'][i] / v1['senti_sum'][i]) + '\n')
                    else:
                        with open(FOLDER_SENTI % k + k1, 'a') as fp2:
                            fp2.write(str(i) + '\t' + str(v1['senti'][i]) + '\n')

def put_statics(s_type, o_type, a_date, o_date, senti):
    if s_type == 'all':
        RESULT['all']['count'][date_diff(a_date, o_date)] += 1
        RESULT['all']['senti'][date_diff(a_date, o_date)] += senti
        RESULT['all']['senti_sum'][date_diff(a_date, o_date)] += 1
    else:
        if not o_type in RESULT[s_type]:
            RESULT[s_type][o_type] = {
                'count': [0] * 61,
                'senti': [0.0] * 61,
                'senti_sum': [0] * 61,
            }
        RESULT[s_type][o_type]['count'][date_diff(a_date, o_date)] += 1
        RESULT[s_type][o_type]['senti'][date_diff(a_date, o_date)] += senti
        RESULT[s_type][o_type]['senti_sum'][date_diff(a_date, o_date)] += 1

def main():
    try:
        create_hist()
        write_result()
    except Exception,e:
        print e
    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()
