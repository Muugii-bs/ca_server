# -*- coding: utf-8 -*-
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


def es_search(field, keyword, start, end):
    query = {
        "from": 0,
        "size": 10000,
        "query": {
            "bool": {
                "must": [
                    {
                        "range": {
                            "date": {
                                "gte": start,
                                "lte": end
                            }
                         },
                    },
                    {
                        "bool": {
                           "should": []
                        }
                    }
                ]
            }
        },
        "sort": [
            {
                "date": { 
                    "order": "asc" 
                }
            },
            { 
                "_score": { 
                    "order": "desc" 
                }
            }
        ]
    }
    keyword = keyword.split('|')
    if len(keyword) > 0:
        for user in keyword:
            query['query']['bool']['must'][1]['bool']['should'].append({"match_phrase": {field: user,}})
    else: 
         query['query']['bool']['must'][1]['bool']['should'].append({"match_phrase": {field: keyword,}})
    print(json.dumps(query))
    return es_query(query)

def es_aggs(field, keyword, start, end):
    query = {
        "size": 0,
        "query": {
            "bool": {
                "should": []
            }
        },
        "aggs": {
            "date_range": {
                "filter": {
                    "range": {
                        "date": {
                            "gte": start,
                            "lte": end
                        }
                    }
                },
                "aggs": {
                    "tweet_histogram": {
                        "date_histogram": {
                            "field": "date",
                            "interval": "day"
                        }
                    }
                }
            }
        }
    }
    keyword = keyword.split('|')
    if len(keyword) > 0:
        for user in keyword:
            query['query']['bool']['should'].append({"match_phrase": {field: user,}})
    else:
        query['query']['bool']['should'].append({"match_phrase": {field: keyword,}})
    print(json.dumps(query))
    return es_query(query)
