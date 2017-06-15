# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 21:42:55 2017

@author: MKD
"""
import pandas as pd                                     #导包
import numpy as np
import re
import time
####################导入数据#############################
N = 100000                                              #样本个数
res=pd.read_csv('res.csv')                              #读取属性数据集
df=pd.read_csv('df.csv')                                #读取规则数据集
df_A = df[(df['target']=='A')]                          #读取属性数据集中target=A的数据集
len_A = len(df_A)                                       #计算target=A的数据集的数量
len_B = 100000-len_A                                    #计算target=B的数据集的数量

###################按照相互等价的为一类分类#################
start_1 = time.time()
rules = res.ix[:,1]                                     #提取规则数据集中的规则列
new_rules = []                                          #创建一个list存放计算过后的规则
reExp1 = r'X(.*?)=(.*?)[,}]'                            #正则表达式过滤条件(提取等号两边的数值，组成一个tuple)
for tup in rules:                                       #遍历所有规则------------>复杂度O(R)
    invert = []                                         #创建一个list存放正则后的结果
    invert = re.compile(reExp1).findall(tup)
    tmp = map(lambda x:int(x[0]) + int(x[1]),invert)    #将每个tuple中的数值相加
    tmp = list(tmp)                                     #将结果转成list类型
    tmp.sort()                                          #将list中数值从小到大排序
    tmp = "".join([str(i) for i in tmp])                #将数值合并成一个数字，(例如[2,8,10]-->[2810])
    new_rules.append(tmp)                               #将结果添加到new_rules
dic_rul = dict(zip((res.ix[:,0]),new_rules))            #新建一个字典，key=规则序号，values=新的rules
rev_dic = {}                                            #新建一个字典存放等价规则分类后的规则，key=rules，values=具有相同rules的rules序号
for k,v in dic_rul.items():                             #遍历dic---------------->复杂度O(R)
    rev_dic.setdefault(v, []).append(k)                 #将相同规则的序号放到一起--->复杂度O(1)
result_1 = pd.DataFrame.from_dict(rev_dic,orient='index')
end_1 = time.time()

####################计算每个类中的最大interest############
start_2 = time.time()
dic_sup = dict(zip((res.ix[:,0]),res.ix[:,2]))          #创建字典存放sup
rul = []                                                #新建list存放规则
interest =[]                                            #新建list存放每个类最大的interest值
for k,v in rev_dic.items():                             #
    NN = []                                             #新建list存放每个key中的所有interest值
    for j in v:                                         #循环每个key对应的values--->前两个循环O(R)
        sup = dic_sup[j]                                #获取对应的规则
        inter = ((N*sup)*(N-N*sup))/(len_A*len_B)       #计算Internet值
        NN.append(inter)                                #将每个key中计算的interest值存放到list中
    K = max(NN)                                         #寻到最大的Internet------>复杂度O(K)
    interest.append(K)                                  #将每个key中的最大Internet添加到list
    rul.append(rules[v[NN.index(max(NN))]])             #寻找最大Internet对应的rules，并添加到list---->复杂度O(R)
result_2 = pd.DataFrame({'interest':interest,'rules':rul},columns=['rules','interest'])
end_2 = time.time()
time_1 = end_1 - start_1
time_2 = end_2 - start_2