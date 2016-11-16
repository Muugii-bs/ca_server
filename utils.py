# -*- coding: utf-8 -*-
import sys
import json
from elasticsearch import Elasticsearch
es = Elasticsearch(['http://127.0.0.1:9200'])

def es_query(query):
    res = es.search(index='ca1', doc_type='tweets', body=query, request_timeout=999999999)
    return res

def es_max_id():
    query = { 
        "aggs": {
            "max_id": { 
                "max" : { 
                    "field" : "id" 
                } 
            } 
        }, 
        "size":0 
    }
    res = es_query(query)
    return int(res['aggregations']['max_id']['value'])


def es_search(keyword, start, end):
    query = {
        "from": 0,
        "size": 10000,
        "query": {
            "bool": {
                "should": [
                    {"bool": {"must":[{"range":{"created":{"gte": start,"lte":end}}},{"match_phrase":{"text":keyword,}}]}},
                    {"bool": {"must":[{"range":{"re_st_created":{"gte":start,"lte":end}}},{"match_phrase":{"re_st_text":keyword,}}]}},
                ]
            }
        }
    }
    return es_query(query)

def es_aggs(field, keyword, start, end):
    prefix = 're_st_' if field == 're_st' else '' 
    query = {
        "size": 0,
        "query": {
            "match_phrase": {
                prefix + 'text': keyword
            }
        },
        "aggs": {
            "date_range": {
                "filter": {
                    "range": {
                        prefix + 'created': {
                            "gte": start,
                            "lte": end
                        }
                    }
                },
                "aggs": {
                    "tweet_histogram": {
                        "date_histogram": {
                            "field": prefix + 'created',
                            "interval": "day"
                        }
                    }
                }
            }
        }
    }
    print(json.dumps(query))
    return es_query(query)

if __name__ == '__main__':
    print(json.dumps(es_search(sys.argv[1], '2016-03-10 00:00:00', '2016-11-11 00:00:00')))
