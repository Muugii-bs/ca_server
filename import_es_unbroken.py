# -*- coding: utf-8 -*-
import json 
import os
import sys

def create_bulk_files():
    dir_list = ['200810','200901','200903','200904','200906','200907','200909','201004']
    for _dir in dir_list:
        path = './' + _dir + '/'
        files = [f for f in os.listdir(path)]
        for f in files:
            if f.endswith('.txt'):
                with open(path + f, 'r') as fp:
                    data = fp.read().replace('\\\n', '').replace('\\\t', '').replace('\\N\t', '')
                    for num,line in enumerate(data.split('\n')):
                        if num % 200000 == 0:
                            file_name = 'bulk_' + str(num) + '_' + f
                            print "Writing to bulk_file......", file_name, num
                            open(file_name, 'w').close()
                        line = line.split('\t')
                        if len(line) != 4: continue
                        index = {'index': {'_index': 'ca', '_type': 'tweets', '_id': line[0]}}
                        data  = {'user': line[1], 'content': line[2], 'date': line[3].replace(' ', '')}
                        with open(file_name, 'a') as fp:
                            fp.write(json.dumps(index) + '\n')
                            fp.write(json.dumps(data) + '\n')

def import_bulk_files():
    cmd = "curl -s -XPOST localhost:9200/_bulk --data-binary \"@%s\" > /dev/null"
    cmv = "mv %s ./imported"
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for f in files:
        if f.startswith('bulk_'):
            print "Importing file.....", f 
            os.system(cmd % f)
            os.system(cmv % f)

if __name__ == '__main__':
    create_bulk_files()
    import_bulk_files()
