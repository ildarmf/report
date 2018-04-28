#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import re

INITIAL_WORD = 'ASSETS'
FINAL_WORD = 'Retained earnings'
SEARCH_WORD = '[T-t]otal.*'

with open('file.json') as fl:
    data = json.load(fl)

data_after_parse = []

for n in data:
  if n['text'] != " \n" and n['text'] != "$ \n" and n['text'] != "$\n":
    if '(' in  n["text"] or ')' in n["text"] or '\n' in n["text"]:
        n["text"] = n["text"].replace('(', '')
        n["text"] = n["text"].replace(')', '')
        n["text"] = n["text"].replace('\n', '').strip()
    data_after_parse.append(n)

sort_data = sorted(data_after_parse, key=lambda i: i['y0'], reverse=True)

for i, x in enumerate(sort_data):
    if x["text"] == INITIAL_WORD:
        position_start = i
    if x["text"] == FINAL_WORD:
        position_end = i
    match = re.search(SEARCH_WORD, x["text"])
    if match:
        del sort_data[i]

data = []
data = sort_data[position_start:position_end+3]


for i, x in enumerate(data):
    if x["text"].isupper():
        print x["text"]


# with open('result.json', 'w') as fl:
#     json.dump(data, fl)
