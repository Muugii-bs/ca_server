from dateutil.relativedelta import relativedelta
from utils import *

import sys
import json
import datetime as dt
import numpy as np

def get_interval(ca_day,date):
    itr = ca_day
    for i in range(1,7):
        if date < itr and date > ca_day + relativedelta(months=-i): return i-1
        itr = ca_day + relativedelta(months=-i) 
    return None

def get_avg(res,cnt):
    base = float(len([x for x in cnt if x > 0]))
    if base == 0.0: return res
    avg  = float(sum(res)) / base
    if avg == 0.0: return res
    return [round(x / avg, 5) for x in res]

def get_stats(dir_in, dir_out):
    sum_hist, sum_senti = [], []
    ca_map = load_json('./result_content_attacker/date_map.json')
    files  = get_files(dir_in + '/', '.txt')
    for file in files:
        target  = file.split('_')[0]
        _type   = file.split('.')[0].split('_')[1]
        ca_day  = get_date(ca_map[target][0])
        res     = [0.0] * 6
        cnt     = [0] * 6
        with open(dir_in + '/' + file, 'r') as fp:
            for line in fp:
                line = line.rstrip().split('\t')
                date = get_date(line[0])
                val  = float(line[1])
                idx  = get_interval(ca_day, date)
                if not idx is None: 
                    res[idx] += val
                    cnt[idx] += 1
            for i in range(0,6):
                if _type == 'senti' and cnt[i] > 0: res[i] = res[i] / cnt[i]
            if _type == 'histogram': res = get_avg(res, cnt) 
            if _type == 'senti': sum_senti.append(res)
            elif _type == 'histogram': sum_hist.append(res)
            with open(dir_out + '/' + file, 'w') as fp1:
                fp1.write(target + '\t\t' + " ,".join(map(str,res)) + '\n')                    
    data1 = np.mean(np.array(sum_hist), axis=0)
    data2 = np.mean(np.array(sum_senti), axis=0)
    print('hist')
    for d in data1:
        print(d)
    print('senti')
    for d in data2:
        print(d)

if __name__ == '__main__':
    get_stats(sys.argv[1], sys.argv[2])
