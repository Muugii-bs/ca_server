# -*- coding: utf-8 -*-
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
term_black_list = ["-", "_", "*", "月", "日", "分", "時", "秒", "時間", "する", "なる", "とる"]
#}}}
def get_filtered_tokens(text):
    parsed = mt.parse(text)
    tokens = []
    for num,line in enumerate(parsed.split('\n')):
        if line == 'EOS' or line == '': continue
        line = line.split()
        desc = line[1].split(',')
        if desc[:2] == ["名詞",   "固有名詞"] or desc[-3] == "*":
            word = line[0]
        else:
            word = desc[-3]
        if not desc[:2] in cat_white_list: continue
        if word in term_black_list: continue
        tokens.append(word)
    return tokens
