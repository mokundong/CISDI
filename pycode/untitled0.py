# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 21:42:55 2017

@author: MKD
"""

import pandas as pd
import numpy as np
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

m=[]
for k,v in rev_dic.items():
    l=[]
    for j in v:
        ex = rules[j-1]
        invert_1 = []
        invert_1 = re.compile(reExp1).findall(ex)
        tmpe = list(map(lambda x :(int(x[0]),int(x[1])),invert_1))
        TL = 74823*[True]
        IN = []
        for ii,jj in tmpe:
            a = df_A.ix[:,ii] == jj
            TL = TL & a
            A = sum(TL)
            inter = (10000*A - A*A)/(74823*25177)
            IN.append(inter)
        
        break
            
#            n.append(h)
#            for i,j in n:
#                print(i,j)
#        break
         
#            TL = 74823*[True]
#            IN = []
#            for i,j in h:
#                print(i,j)
#                a = df_A.ix[:,i] == j
#                TL = TL & a
#                A = sum(TL)
#                interest = (10000*A - A*A)/(74823*25177) 
#                IN.append(interest)
