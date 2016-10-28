# -*- coding: utf-8 -*-
import sys
import json
import operator

from mecab_utils import get_filtered_tokens, load_senti_verb
from es_utils import es_search, es_aggs

def tweet_count(res):
    keyword_count = {}
    for bucket in res['aggregations']['date_range']['tweet_histogram']['buckets']:
        day = bucket['key_as_string'][:10]
        keyword_count[day] = bucket['doc_count']
    sorted_count = sorted(keyword_count.items(), key=operator.itemgetter(0))
    with open('histogram.txt', 'w') as fp:
        for pair in sorted_count:
            fp.write(pair[0] + '\t' + str(pair[1]) + '\n')

def keyword_count(res):
    senti_map = load_senti_verb()
    with open('dict.json', 'w') as fp:
        json.dump(senti_map, fp)
    senti_sum = {}
    keywords  = {}
    for hit in res['hits']['hits']:
        day   = hit['_source']['date'][:10]
        words = get_filtered_tokens(hit['_source']['content'])
        if not day in senti_sum: senti_sum[day] = 0
        for word in words:
            if not word in keywords: keywords[word] = 0
            keywords[word] += 1
            if word in senti_map: 
                senti_sum[day] += senti_map[word] 
        if len(words) > 0:
            senti_sum[day] = float(senti_sum[day]) / float(len(words))
    sorted_senti_sum = sorted(senti_sum.items(), key=operator.itemgetter(0))
    sorted_keywords  = sorted(keywords.items(), key=operator.itemgetter(1), reverse=True)
    with open('senti.txt', 'w') as fp:
        for pair in sorted_senti_sum:
            fp.write(pair[0] + '\t' + str(pair[1]) + '\n')
    with open('keywords.txt', 'w') as fp:
        for pair in sorted_keywords:
            fp.write(pair[0].encode('utf-8') + '\t' + str(pair[1]) + '\n')

def main():
    job_type = sys.argv[1]
    keyword  = sys.argv[2]
    start    = sys.argv[3]
    end      = sys.argv[4]
    if job_type == 'query_content':
        res = es_search('content', keyword, start, end)
        with open('res.json', 'w') as fp:
            json.dump(res, fp)
        keyword_count(res)
        res = es_aggs('content', keyword, start, end)
        tweet_count(res)    
    elif job_type == 'query_user':
        res = es_search('user', keyword, start, end)
        keyword_count(res)
        res = es_aggs('user', keyword, start, end)
        tweet_count(res)
    else:
        print("type error!")
        exit()

if __name__ == '__main__':
    main()
