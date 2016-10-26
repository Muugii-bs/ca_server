# -*- coding: utf-8 -*-
import sys
import json
from es_utils import es_query

keyword = sys.argv[1]
query = {
    "size": 100,
    "query": {
        "match": {
            "content": keyword,
            #"fields": ["content", "user"],
            #"type": "phrase"
        }
    }
}
"""
"sort": [
    { 
        "_score": { 
            "order": "desc" 
        }
    },
    {
        "date": { 
            "order": "desc" 
        }
    }
]
"""

res = es_query(query)

print(json.dumps(res))
