# -*- coding: utf-8 -*-
import json
from elasticsearch import Elasticsearch
es = Elasticsearch(['http://127.0.0.1:9200'])

def es_query(query):
    print json.dumps(query)
    res = es.search(index='ca', doc_type='tweets', body=query, request_timeout=999999999)
    return res

