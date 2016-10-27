# -*- coding: utf-8 -*-
import json
from elasticsearch import Elasticsearch
es = Elasticsearch(['http://127.0.0.1:9200'])

def es_query(query):
    res = es.search(index='ca', doc_type='tweets', body=query, request_timeout=999999999)
    return res

def es_search(field, keyword, start, end):
    query = {
        "from": 0,
        "size": 10000,
        "query": {
            "bool": {
                "must": [
                    {
                        "match_phrase": {
                            field: keyword,
                        }
                    },
                    {
                        "range": {
                            "date": {
                                "gte": start,
                                "lte": end
                            }
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
    return es_query(query)

def es_aggs(field, keyword, start, end):
    query = {
        "size": 0,
        "query": {
            "match_phrase": {
                field: keyword,
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
    return es_query(query)
