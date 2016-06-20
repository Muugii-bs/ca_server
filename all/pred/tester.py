import json
import sys

with open(sys.argv[1], 'r') as fp:
    print json.load(fp)
