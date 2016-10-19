# -*- coding: utf-8 -*-
import json 
import os

with open('TEXT.TXT', 'r') as fp:
    data = fp.read().replace('\\\n', '').replace('\\\t', '').replace('\\N\t', '')

prefix = '_data.tsv'
for num,line in enumerate(data.split('\n')):
    if num % 1000000 == 0:
        file_name = str(num) + prefix
        print "Writing to bulk_file......", file_name, num
        open(file_name, 'w').close()
    line = line.split('\t')
    if len(line) != 4: continue
    index = {'index': {'_index': 'ca', '_type': 'tweets', '_id': line[0]}}
    data  = {'user': line[1], 'content': line[2], 'date': line[3].replace(' ', '')}
    with open(file_name, 'a') as fp:
        fp.write(json.dumps(index) + '\n')
        fp.write(json.dumps(data) + '\n')

cmd = "curl -s -XPOST localhost:9200/_bulk --data-binary \"@%s\" > /dev/null"
cmv = "mv %s ./imported"
files = [f for f in os.listdir('.') if os.path.isfile(f)]
for f in files:
    if f.endswith('_data.tsv'):
        print "Importing file.....", f 
        os.system(cmd % f)
        os.system(cmv % f)
