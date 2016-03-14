# -*- coding: utf-8 -*-
from TwitterSearch import *
from pprint import pprint
import mysql.connector as db
import time
import json
import sys

class MySQLConverter(db.conversion.MySQLConverter):
    """ A mysql.connector Converter that handles Numpy types """

    def _float32_to_mysql(self, value):
        return float(value)

    def _float64_to_mysql(self, value):
        return float(value)

    def _int32_to_mysql(self, value):
        return int(value)

    def _int64_to_mysql(self, value):
        return int(value)

db_config = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': 'root',
        'database': 'cnl',
        'autocommit': True,
        'raise_on_warnings': True,
}
conn = db.connect(**db_config)
conn.set_converter_class(MySQLConverter)
cursor = conn.cursor()
cursor1 = conn.cursor()

def move_db():
    query = "SELECT name, clan, tweet, date FROM tweets GROUP BY tweet"
    cursor.execute(query)
    for row in cursor:
        cursor1.execute("INSERT INTO tweets_new (name, clan, tweet, date) VLAUES(%s, %s, %s, %s)", (row['name'], row['cnan'], row['tweet'], row['date']))

def main():
    move_db()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()
