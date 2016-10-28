from sklearn.cluster import KMeans 

import pymysql as db
import numpy as np
import operator as op
import datetime as dt
import sys

def run(attack_id, keyword, clusters, sampling):
    db_config = {
        'host':     '127.0.0.1',
        'port':     3306,
        'user':     'root',
        'passwd':   'root',
        'db':       'cnl'
    }
    conn = db.connect(**db_config)
    cursor = conn.cursor()
    keywords = keyword_master(cursor, attack_id, keyword, sampling)
    dataset, desc = create_dataset(cursor, keywords, attack_id, keyword)
    kmeans = KMeans(n_clusters=clusters, random_state=0).fit(dataset)
    np.save('labels.npy', np.array(kmeans.labels_))
    sql = "DELETE FROM ca_kmeans WHERE attack_id=%s"
    cursor.execute(sql % attack_id)
    conn.commit()
    for num,label in enumerate(kmeans.labels_):
        sql = """
            INSERT IGNORE INTO ca_kmeans 
              (attack_id, content_id, cluster_id, date_diff) 
              VALUES(%s, %s, %s, %s)
            """
        cursor.execute(sql, (desc[num][0], desc[num][1], label.astype('str'), desc[num][2]))
        conn.commit()
    cursor.close()
    conn.close()

def create_dataset(cursor, keywords, attack_id, keyword):
    dataset, desc = [], []
    sql = """
        SELECT id, content, date, date_orig FROM ca_analyze
        WHERE attack_id=%s
        AND content LIKE '%%%s%%'
        """
    cursor.execute(sql % (attack_id, keyword))
    for row in cursor:
        tmp = [0] * len(keywords)
        diff = get_datetiff(row[2], row[3])
        for word in row[1].rstrip().split():
            if word in keywords: tmp[keywords[word]] += 1
        dataset.append(tmp)
        desc.append([attack_id, row[0], diff])
    return np.array(dataset), desc

def get_datetiff(date, date_orig):
    if date is None or date_orig is None:
        return 9999
    return (date - date_orig).days

def keyword_master(cursor, attack_id, keyword, sampling):
    keywords = {}
    with open('keywords_%s.tsv' % attack_id, 'r') as fp:
        cnt = sum(1 for line in fp)
    with open('keywords_%s.tsv' % attack_id, 'r') as fp:
        for num,line in enumerate(fp):
            if num > int(cnt/sampling): break
            keywords[line.split('\t')[0]] = num
    return keywords

def main():
    run(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))

if __name__ == '__main__':
    main()

