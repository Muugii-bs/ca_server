import mysql.connector as db
import json

db_config = {
		'host':				'127.0.0.1',
		'user':				'root',
		'password':		'root',
                'port':				3306,
		'database':		'cnl',
		'autocommit':	True,
	}

conn = db.connect(**db_config)
conn1 = db.connect(**db_config)
cursor = conn.cursor()
cursor1 = conn1.cursor()

def set_new_flag():
    cursor.execute('UPDATE ca_analyze SET new_flag=1 WHERE date_orig <> "0000-00-00" AND date_orig IS NOT NULL')

def copy_to_new_table():
    cursor.execute('SELECT date,author,target,attack_type,attack_category,target_category,country,attack_id,count,content,media,url,date_orig,new_flag FROM ca_analyze WHERE new_flag = 1')
    for row in cursor:
        cursor1.execute('INSERT INTO ca_analyze_new (date,author,target,attack_type,attack_category,target_category,country,attack_id,count,content,media,url,date_orig,new_flag) VALUES (%s,%s,%s,%s,%s,%s,%s,%d,%d,%s,%s,%s,%s,%d)', (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13]))
        
def main():
	set_new_flag()

if __name__ == '__main__':
	main()
