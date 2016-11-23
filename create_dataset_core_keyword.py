from config import db_config
from utils import *

import pymysql as db
import numpy as np

conn = db.connect(**db_config)
cursor = conn.cursor()

def create_dataset():
    dataset, testset = [], []
    SCORES  = load_score_master()
    core    = load_annotation('exploits.tsv')
    K       = Keyword('keyword_master.txt', 4000)
    query = """
            SELECT software_list, score, access_vector, 
              access_complexity, authentication, confidentiality_impact, 
              integrity_impact, availability_impact, id, exploit_type, entry_id, summary
            FROM vuln_analyze 
            WHERE exploit_type IS NOT NULL 
              AND entry_id IN ('%s')
            ORDER BY RAND() """
    cursor.execute(query % "','".join(list(core.keys())))
    for row in cursor.fetchall():
        tmp = [None] * 8
        tmp[0] = float(SCORES['layer'][fetch_layer_sum(row[0])])
        tmp[1] = float(row[1])
        tmp[2] = float(SCORES['access_vector'][row[2]])
        tmp[3] = float(SCORES['access_complexity'][row[3]])
        tmp[4] = float(SCORES['authentication'][row[4]])
        tmp[5] = float(SCORES['confidentiality_impact'][row[5]])
        tmp[6] = float(SCORES['integrity_impact'][row[6]])
        tmp[7] = float(SCORES['availability_impact'][row[7]])
        tmp.extend(K.get_vector(get_tokens(row[11])))
        
        label = fetch_label(row[9], core[row[10]], 'core')
        if 1 in label:
            tmp.append(label.index(1))
            dataset.append(tmp)
    '''
    query = """
            SELECT software_list, score, access_vector, 
              access_complexity, authentication, confidentiality_impact, 
              integrity_impact, availability_impact, id, exploit_type, entry_id
            FROM vuln_analyze 
            WHERE exploit_type IS NOT NULL 
              AND entry_id NOT IN ('%s')
            ORDER BY RAND() """
    cursor.execute(query % "','".join(list(core.keys())))
    for row in cursor.fetchall():
        tmp = [None] * 8
        tmp[0] = float(SCORES['layer'][fetch_layer_sum(row[0])])
        tmp[1] = float(row[1])
        tmp[2] = float(SCORES['access_vector'][row[2]])
        tmp[3] = float(SCORES['access_complexity'][row[3]])
        tmp[4] = float(SCORES['authentication'][row[4]])
        tmp[5] = float(SCORES['confidentiality_impact'][row[5]])
        tmp[6] = float(SCORES['integrity_impact'][row[6]])
        tmp[7] = float(SCORES['availability_impact'][row[7]])
        #tmp.extend(line.get_line(row[8])) 
        label = fetch_label(row[9], '', 'test')
        if 1 in label:
            tmp.append(label.index(1))
            testset.append(tmp)
    '''
    cursor.close()
    conn.close()
    '''
    testset = np.array(testset)
    np.random.shuffle(testset)
    np.save('data/testset.npy', testset)
    '''
    dataset = np.array(dataset)
    np.random.shuffle(dataset)
    np.save('data/dataset.npy', dataset)

if __name__ == '__main__':
    create_dataset()
