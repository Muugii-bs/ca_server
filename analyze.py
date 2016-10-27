# -*- coding: utf-8 -*-
import sys
import json
from mecab_utils import get_filtered_tokens
from es_utils import es_search, es_aggs

def keyword_count(res):
    print "hh"    

def main():
    job_type = sys.argv[1]
    keyword  = sys.argv[2]
    start    = sys.argv[3]
    end      = sys.argv[4]
    if job_type == 'query_content':
        print(json.dumps(es_search('content', keyword, start, end)))
    elif job_type == 'query_user':
        print(json.dumps(es_search('user', keyword, start, end)))
    elif job_type == 'aggs_user':
        print(json.dumps(es_aggs('user', keyword, start, end)))
    elif job_type == 'aggs_content':
        print(json.dumps(es_aggs('content', keyword, start, end)))
    else:
        print("type error!")
        exit()

if __name__ == '__main__':
    main()
