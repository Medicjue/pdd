#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  4 00:03:00 2019

@author: Julius
"""

import pandas as pd

alexa_top1m = pd.read_csv('../data/top-1m.csv', names=['rank', 'domain'])

#%%

words = 'abcdefghijklmnopqrstuvwxyz0123456789'

alxea_lists = dict()

for index, row in alexa_top1m.iterrows():
    domain = row['domain']
    char = domain[0:1]
    alxea_list = alxea_lists.get(char)
    if alxea_list is None:
        alxea_list = []
        alxea_lists[char] = alxea_list
    alxea_list.append(domain)
    
for word in words:
    with open('../data/alexa-tld/{}.txt'.format(word), 'w', encoding='utf8') as f:
        alxea_list = alxea_lists.get(word)
        for domain in alxea_list:
            f.write(domain)
            f.write('\n')
        f.flush()