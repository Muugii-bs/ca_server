import pymysql as db
from pprint import pprint

#{{{
db_config = {
    'host':	    '127.0.0.1',
    'port':	    3306,
    'user':	    'root',
    'passwd':	    'root',
    'db':	    'cnl',
    'autocommit':   True,
}
stop_words = [
    'makes', 'make', 'allows', 'allow', 'has', 'have'
]
#}}}

conn = db.connect(**db_config)
cursor = conn.cursor()
conn1 = db.connect(**db_config)
cursor1 = conn1.cursor()

def get_summary_short():
    for word in stop_words:
        sql = "SELECT id, summary FROM vuln_analyze WHERE summary LIKE '%% %s %%' " % word
        cursor.execute(sql)
        for i in range(0, cursor.rowcount):
            row = cursor.fetchone()
            summary_short = row[1].split(' %s ' % word)[1]
            sql1 = "UPDATE vuln_analyze SET summary_short=%s WHERE id=%s"
            cursor1.execute(sql1, (summary_short, row[0]))

def main():
    get_summary_short()
    cursor.close()
    conn.close()
    cursor1.close()
    conn1.close()

if __name__ == '__main__':
    main()
