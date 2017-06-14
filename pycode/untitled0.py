# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 21:42:55 2017

@author: MKD
"""

import pandas as pd
import time
import re

res=pd.read_csv('res.csv')
df=pd.read_csv('df.csv')
df_A = df[(df['target']=='A')]

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
dic = dict(zip((res.ix[:,0]),new_rules))
rev_dic = {}
for k,v in dic.items():
    rev_dic.setdefault(v, []).append(k)
    
    
###########################################
#d={'819': [572, 581, 1593, 1601, 2084, 2085, 2097, 2346, 2347, 2359],
# '2519': [31434, 31443, 48261, 48270, 51163, 51408],
# '31214': [21648, 21651, 21652, 21669, 21674, 22189, 22277, 22302]}
#
rul = []
interest =[]
for k,v in rev_dic.items():
    NN=[]
    for j in v:
        ex = rules[j-1]
        invert = []
        invert = re.compile(reExp1).findall(ex)
        tmpe = list(map(lambda x :(int(x[0]),int(x[1])),invert))
        TL = 74823*[True]
        IN = []
        for sing_tmpe in tmpe:
            b = df_A.ix[:,sing_tmpe[0]] == sing_tmpe[1]
            TL = TL & b
            A = sum(TL)
        inter = (100000*A - A*A)/(74823*25177)
        NN.append(inter)
    N = max(NN)
    interest.append(N)
    rul.append(rules[v[NN.index(max(NN))]])
result = pd.DataFrame({'interest':interest,'rules':rul},columns=['rules','interest'])