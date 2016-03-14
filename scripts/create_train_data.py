import mysql.connector as db
import sys
import os
import json
import operator
from itertools import izip
from random import randint

ATTACK_TYPE = 'Account Hijacking'
TRAIN_COUNT = 400
TEST_COUNT = 90
FILE_TRAIN = 'Train_' + ATTACK_TYPE.replace(' ', '')
FILE_TEST = 'Test_' + ATTACK_TYPE.replace(' ', '')

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

def init():
	os.system('rm ' + FILE_TRAIN)
	os.system('rm ' + FILE_TEST)

def on_ids():
	query = "SELECT DISTINCT feature_1000 FROM ca_analyze WHERE flag='on' AND attack_type=%s"
	cursor.execute(query, (ATTACK_TYPE,))
	rows = cursor.fetchall()
	
	for i in range(0, TRAIN_COUNT):
		content = json.loads(rows.pop(0)[0])
		line = '1 '
		for i in range(1, 1001):
			line = line + str(i) + ':' + str(content[i-1]) + ' '
		line += '\n'
		with open(FILE_TRAIN, 'a') as fp:
			fp.write(line)

	for j in range(0, TEST_COUNT):
		content = json.loads(rows.pop(0)[0])
		line = '1 '
		for i in range(1, 1001):
			line = line + str(i) + ':' + str(content[i-1]) + ' '
		line += '\n'
		with open(FILE_TEST, 'a') as fp:
			fp.write(line)

def off_ids():
	query = "SELECT DISTINCT feature_1000 FROM ca_analyze WHERE flag='off' AND attack_type=%s"
	cursor.execute(query, (ATTACK_TYPE,))
	rows = cursor.fetchall()
	cnt = len(rows)
	itr = 0
	for i in range(0, TRAIN_COUNT):
		content = json.loads(rows.pop(itr)[0])
		cnt -= 1
		itr = randint(0, cnt - 1)
		line = '0 '
		for i in range(1, 1001):
			line = line + str(i) + ':' + str(content[i-1]) + ' '
		line += '\n'
		with open(FILE_TRAIN, 'a') as fp:
			fp.write(line)

	for i in range(0, TEST_COUNT):
		content = json.loads(rows.pop(itr)[0])
		cnt -= 1
		itr = randint(0, cnt - 1)
		line = '0 '
		for i in range(1, 1001):
			line = line + str(i) + ':' + str(content[i-1]) + ' '
		line += '\n'
		with open(FILE_TEST, 'a') as fp:
			fp.write(line)

def main():
	init()
	on_ids()
	off_ids()
	conn.close()

if __name__ == '__main__':
	main()

