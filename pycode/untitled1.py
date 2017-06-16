# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 21:13:40 2017

@author: MKD
"""
import pandas as pd
import time
import re

def findMaxloca(lists):
    key = [i for i in range(len(lists))]
    dic = dict(zip(key,lists))
    dicc = {}
    for k,v in dic.items():
        dicc.setdefault(v,[]).append(k)
    return dicc[max(lists)]

def loadData(dfpath,respath):
    df = pd.read_csv(dfpath)
    res = pd.read_csv(respath)
    df_A = df[(df['target'] == 'A')]
    len_A = len(df_A)
    len_B = 100000 - len_A
    return res,df,df_A,len_A,len_B
    
def classRules(res,rules):
    starttime = time.time()
    new_rules = []
    rev_dic = {}
    reExp = r'X(.*?)=(.*?)[,}]'
    for rule in rules:
        invert = []
        invert = re.compile(reExp).findall(rule)
        tmp_1 = map(lambda x:int(x[0]) + int(x[1]),invert)
        tmp_2 = list(tmp_1)
        tmp_2.sort()
        tmp = "".join([str(i) for i in tmp_2])
        new_rules.append(tmp)
    dic_rul = dict(zip((res.ix[:,0]),new_rules))
    for k,v in dic_rul.items():
        rev_dic.setdefault(v,[]).append(k)
    endtime = time.time()
    totaltime = endtime - starttime
    return rev_dic,totaltime
    

def findMaxInterestOfEachclass(res,rules,N,rev_dic,len_A,len_B):
    starttime = time.time()
    dic_sup = dict(zip((res.ix[:,0]),res.ix[:,2]))
    ruless = []
    interest = []
    for k,v in rev_dic.items():
        interOfEachRule = []
        for num in v:
            sup = dic_sup[num]
            inter = ((N*sup)*(N-N*sup))/(len_A*len_B)
            interOfEachRule.append(inter)
        MaxInterOfEachRule = max(interOfEachRule)
        interest.append(MaxInterOfEachRule)
        ruless.append(rules[v[interOfEachRule.index(MaxInterOfEachRule)]])
    endtime = time.time()
    totaltime = endtime - starttime
    return interest,ruless,totaltime

if __name__ == '__main__':
    N = 100000
    dfpath = 'df.csv'
    respath = 'res.csv'
    #加载数据
    res,df,df_A,len_A,len_B = loadData(dfpath,respath)
    rules = res.ix[:,1]
    rev_dic,time1 = classRules(res,rules)
    interest,rules,time2 = findMaxInterestOfEachclass(res,rules,N,rev_dic,len_A,len_B)
    result_1 = pd.DataFrame.from_dict(rev_dic,orient='index')
    result_2 = pd.DataFrame({'interest':interest,'rules':rules},columns=['rules','interest'])