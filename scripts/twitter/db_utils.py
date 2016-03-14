import mysql.connector as db
import json
import sys

db_config = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': 'root',
        'database': 'cnl',
        'raise_on_warnings': True,
}

conn = db.connect(**db_config)
cursor = conn.cursor()

def import_accounts(fp, clan):
    with open(fp, 'r') as fp:
        accounts = json.load(fp)
    for user in accounts[clan]:
        query = 'INSERT IGNORE INTO accounts (name, clan) VALUES(%s, %s)'
        cursor.execute(query, (user, clan))
    
def main():
    import_accounts('accounts.json', sys.argv[1])
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()

        
