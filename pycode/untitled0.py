# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 21:42:55 2017

@author: MKD
"""

import pandas as pd
import numpy as np
res=pd.read_csv('res.csv')
import re

rules = res.ix[:,1]
new_rules = []
reExp1 = r'X(.*?)=(.*?)[,}]'
for tup in rules:
    invert = []
    invert = re.compile(reExp1).findall(tup)
    tmp = map(lambda x:int(x[0]) + int(x[1]),invert)
    tmp = list(tmp)
    tmp.sort()
    tmp = "".join([str(i) for i in tmp])
    new_rules.append(tmp)
dic = dict(zip(res.ix[:,0],new_rules))
rev_dic = {}
for k,v in dic.items():
    rev_dic.setdefault(v, []).append(k)
    
    
###########################################
df=pd.read_csv('df.csv')
target_col = df.ix[:,16]
A=B=0
for col in target_col:
    if col == 'A':
        A = A + 1
    else:
        B = B + 1
