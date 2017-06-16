# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 09:22:57 2017

@author: yousa
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 21:13:40 2017

@author: MKD
"""

import pandas as pd
import time
import re

def loadData(dfpath,respath):               #加载数据集
    df = pd.read_csv(dfpath)                
    res = pd.read_csv(respath)
    df_A = df[(df['target'] == 'A')]        #target=A的数据集
    len_A = len(df_A)                       #target=A的数据集大小
    len_B = 100000 - len_A                  #target!=A的数据集大小
    return res,df,df_A,len_A,len_B          #返回相关数据集和数据大小
    
def findMaxloca(lists):                     #求一个列表最大值的位置（其中最大值不止一个）
    key = [i for i in range(len(lists))]    #计算传入list的长度,O(1)
    dic = dict(zip(key,lists))              #生成一个字典，key=序号，v=值，O(n)
    dicc = {}                               #新建字典，key=规则，value=具有等价规则的规则序号
    for k,v in dic.items():                 #遍历字典，key=值，value=最大值的位置
        dicc.setdefault(v,[]).append(k)
    return dicc[max(lists)]                 #返回一个list，内容是最大值的位置

def preproccess(res):                       #数据预处理
    rules = res.ix[:,1]                     #res数据集中rules列
    new_rules = []                          #新建list，存放预处理后的规则                           
    reExp = r'X(.*?)=(.*?)[,}]'             #正则表达式,提取等号两边的数字（Xi=j）-->(i,j)
    for rule in rules:                      #遍历rules列，O(R)
        invert = []
        invert = re.compile(reExp).findall(rule)
        tmp_1 = map(lambda x:int(x[0]) + int(x[1]),invert)#[(i,j),(m,n)]-->[(i+j),(m+n)]
        tmp_2 = list(tmp_1)                 #map函数转换为list
        tmp_2.sort()                        #从小到大排序，O(KlogK)
        tmp = "".join([str(i) for i in tmp_2])#O(K)
        new_rules.append(tmp)               #O(1)
    dic_rul = dict(zip((res.ix[:,0]),new_rules))#新建字典，key=规则序号，values=新的rules，O(R)
    ###
    dic_sup = dict(zip((res.ix[:,0]),res.ix[:,2]))#创建字典存放支持度suport
    return dic_rul,rules,dic_sup             #返回预处理好的规则，和规则列
    
def classRules(dic_rul):                    #按照规则相同的分为一类,输入为预处理好的数据集
    starttime = time.time()
    rev_dic = {}
    for k,v in dic_rul.items():             #遍历上述字典，O(R)
        rev_dic.setdefault(v,[]).append(k)  #本字典key=等价的rule,value=rule对应的规则序号，O(1)
    endtime = time.time()
    totaltime = endtime - starttime
    return rev_dic,totaltime                #返回分类结果和运行时间

def findMaxInterestOfEachclass(rules,rev_dic,dic_sup,N,len_A,len_B):
    starttime = time.time()   
    rulesss = []                            #存放Internet对应的的rules
    interest = []                           #输出rules对应的最大interest值
    for k,v in rev_dic.items():             #遍历字典key=等价的rule,value=rule对应的规则序号，O(k)
        interOfEachRule = []                #存放同一等价规则的intersect值
        for num in v:                       #O(v)
            sup = dic_sup[num]              #查找该规则序号对应的sup值，O(1)
            inter = ((N*sup)*(N-N*sup))/(len_A*len_B)#计算Internet
            interOfEachRule.append(inter)   #同一等价规则的interest
        MaxInterOfEachRule = max(interOfEachRule)#查找最大interest，O(v)
        interest.append(MaxInterOfEachRule) #添加到list,O(1)
        lists = findMaxloca(interOfEachRule)#查找最大值对应的rules(可能不止一个),O(v)
        ruless = []
        for i in lists:                     #遍历lists,寻找左右最大值对应的rules，O(1)
            ruless.append(rules[v[lists.index(i)]])#经过验证，本数据中不存在多个规则对应一个最大值
        rulesss.append(ruless)
    endtime = time.time()
    totaltime = endtime - starttime
    result = dict(zip(rules,interest))
    return result,totaltime                 #返回输出结果，计算时间

if __name__ == '__main__':
    N = 100000
    dfpath = 'df.csv'
    respath = 'res.csv'
    #加载数据
    res,df,df_A,len_A,len_B = loadData(dfpath,respath)
    #数据预处理
    dic_rul,rules,dic_sup = preproccess(res)
    #按照规则相同的分为一类
    result1,time1 = classRules(dic_rul)
    #找到interest对应的rules
    result2,time2 = findMaxInterestOfEachclass(rules,result1,dic_sup,N,len_A,len_B)
    result_1 = pd.DataFrame.from_dict(result1,orient='index')
    result_2 = pd.DataFrame.from_dict(result2,orient='index')
	print(time1,time2)
	result_1.to_csv('rsult1.csv')
	result_2.to_csv('result2.csv')