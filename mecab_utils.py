# -*- coding: utf-8 -*-
import mojimoji 
import MeCab
import sys
import json
#{{{
mt = MeCab.Tagger("mecabrc")
cat_white_list = [
        ["感動詞", "*"],
        ["形容詞", "自立"],
        ["形容詞", "非自立"],
        ["動詞",   "自立"],
        ["副詞",   "一般"],
        ["名詞",   "サ変接続"],
        ["名詞",   "ナイ形容詞語幹"],
        ["名詞",   "一般"],
        ["名詞",   "引用文字列"],
        ["名詞",   "形容動詞語幹"],
        ["名詞",   "固有名詞"],
        ["名詞",   "副詞可能"]
    ]
term_black_list = ["-", "_", "*", "月", "日", "分", "時", "秒", "時間", "する", 
                  "なる", "とる", "", "th", ":", ";", "/", "//", "://", ".", "..", 
                  "...", "..", "(", ")", "|", "｜", "[", "]", "{", "}", ",", "）", "（", "』", 
                  "『", "@", "｀", "`", "”", "’", "_", "＝", "ー", "・", "」", "「",
                  "。", "、", "：", "；", "-", "=", "+", "com", "http", "www", "https"
                  "co", "jp", "info", "org", "cｏ", "\""]
#}}}
def get_filtered_tokens(text):
    parsed = mt.parse(text.encode('utf-8'))
    tokens = []
    for num,line in enumerate(parsed.split('\n')):
        if line == 'EOS' or line == '': continue
        line = line.split()
        if not len(line) > 1: continue
        desc = line[1].split(',')
        if desc[:2] == ["名詞",   "固有名詞"] or desc[-3] == "*":
            word = line[0]
        else:
            word = desc[-3]
        if not desc[:2] in cat_white_list: continue
        if word in term_black_list: continue
        tokens.append(word)
    return tokens

def load_senti_noun(res):
    senti_map = {
        'ポジ': 1,
        'ネガ': -1
    }
    with open('senti_noun.txt', 'r') as fp:
        for num,line in enumerate(fp):
            line = line.rstrip()
            line = line.split('\t')
            if len(line) < 2: continue
            label = line[0].split('（')[0]
            word  = line[1].split()[0]
            if word in res: continue 
            res[word] = senti_map[label]
    return res

def load_senti_verb():
    res = {}
    senti_map = {
        'p': 1,
        'e': 0,
        'n': -1,
        'a': 0,
        '?p?n': 0,
        '?e':  0,
        'o': -1,
        '?p?e': 1,
        '?p': 1
    }
    with open('senti_verb.txt', 'r') as fp:
        for num,line in enumerate(fp):
            line = line.rstrip()
            line = line.split('\t')
            word = mojimoji.zen_to_han(unicode(line[0], 'utf-8'), kana=False)
            if word in res: continue
            if not line[1] in senti_map: continue
            label = senti_map[line[1]]
            res[word] = label
    res = load_senti_noun(res)
    return res
