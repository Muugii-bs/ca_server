import os
import json
import datetime as dt


def get_files(_dir, suffix):
    return [file for file in os.listdir(_dir) if file.endswith(suffix)]

def get_date(_str):
    return dt.datetime.strptime(_str, '%Y-%m-%d')

def get_str(_date):
    return dt.datetime.strftime(_date, '%Y-%m-%d')

def load_json(_file):
    with open(_file, 'r') as fp:
        return json.load(fp)
