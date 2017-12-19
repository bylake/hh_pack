# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np


# import matplotlib.pyplot as plt


# # 对内申请评分模型

# # 1，模型分值

# # 2，管理级别  


# # 3，婚姻状况marry_status 

# In[4]:

def marry(x):
    if pd.notnull(x):

        if x == '已婚':
            return 10
        elif x == '单身':
            return -5
        else:
            return 0
    else:
        return 0

# # 4，工作年限

# In[3]:

# ‘工作年限’字段数值映射
def job_time(x):
    if pd.notnull(x):

        if x > 180:
            return 5
        elif (x > 120) & (x <= 180):
            return 4
        elif (x > 120) & (x <= 180):
            return 3
        elif (x > 60) & (x <= 120):
            return 3
        elif (x > 36) & (x <= 60):
            return 2
        elif (x > 0) & (x <= 36):
            return 1
        else:
            return 0
    else:
        return 0


# # 5，用工形式

# In[2]:

# ‘工作’字段数值映射
def work_form(x):
    if pd.notnull(x):

        if x == '正式员工':
            return 5
        elif x == '试用期员工':
            return -2
        elif x == '劳务派遣人员':
            return -5
        else:
            return 0
    else:
        return 0


# # 6，进入集团时间’字段数值映射

# In[1]:

# ‘进入集团时间’字段数值映射
def company_time(x):
    if pd.notnull(x):

        if x > 180:
            return 20
        elif (x > 120) & (x <= 180):
            return 15
        elif (x > 120) & (x <= 180):
            return 70
        elif (x > 60) & (x <= 120):
            return 10
        elif (x > 36) & (x <= 60):
            return 5
        elif (x > 12) & (x <= 36):
            return 2
        else:
            return 0
    else:
        return 0


# # 7，多头申请

# In[1]:

def many_apply(x):
    if x:

        type1, type2, type3, type4 = x[0]['res'], x[1]['res'], x[2]['res'], x[3]['res']
        if type1 == '是':  # 30天内命中银行多头申请
            score1 = -10
        else:
            score1 = 0

        if type2 == '是':  # 90天内命中银行多头申请
            score2 = -5
        else:
            score2 = 0

        if type3 == '是':  # 180天内命中银行多头申请
            score3 = -2
        else:
            score3 = 0

        if type4 == '是':  # 360天内命中非银多头申请
            score4 = -20
        else:
            score4 = 0

        score = [score1, score2, score3]
        score_dic = {0: -10, 1: -5, 2: -2}
        loc = next((i for i, x in enumerate(score) if x), None)
        if loc:
            sub_score = score_dic[loc]
        else:
            sub_score = 0

        Tscore = sub_score + score4
    else:
        Tscore = 0
    return Tscore


# # 8社会公共治安


def public_score(x):
    if pd.notnull(x):

        if x[0] == '1':  # 吸毒

            score1 = -50
        else:
            score1 = 0

        if x[1] == '1':  # 涉毒
            score2 = -100
        else:
            score2 = 0

        if x[2] == '1':  # 在逃
            score3 = -200
        else:
            score3 = 0

        if x[3:5] == '00':
            score4 = 0
        elif x[3:5] == '10':  # 5-10年前科
            score4 = -100
        elif x[3:5] == '01':  # 5年内前科
            score4 = -150
        elif x[3:5] == '11':  # 10年以上前科
            score4 = -50

        score = score1 + score2 + score3 + score4
    else:
        score = 0

    return score


# # 9.惩罚次数

# In[9]:

def punish(x):
    if pd.notnull(x):

        if x >= 10:
            return -20
        elif x < 3 and x > 0:
            return -5
        elif (x >= 3) & (x <= 10):
            return -15
        else:
            return 0
    else:
        return 0


# # 10个人履约能力是否匹配到  

# In[10]:

def LvYue(x):
    if pd.notnull(x):

        if x > 75:
            return 10
        elif (x >= 62) & (x <= 75):
            return 8
        elif (x >= 51) & (x <= 61):
            return 6
        elif (x >= 44) & (x <= 50):
            return 4
        else:
            return 2
    else:
        return 2


import datetime


def punish_types(d):
    if d:

        punish_field = []
        for i in np.arange(len(d)):

            x = d[i]['vcname']
            t = datetime.datetime.now().year - int(d[i]['vcdispatchdate'][:4])
            a = x.count('警告') > 0 or x.count('批评') > 0 or x.count('记过') > 0
            b = x.count('降级') > 0 or x.count('降职') > 0 or x.count('免职') > 0 or x.count('撤职') > 0 or x.count('停职') > 0
            c = x.count('留用察看') > 0 or x.count('解除劳动合同') > 0
            if c is True:
                s = -300  # '留用察看、解除劳动合同
            elif b is True and t <= 1:
                s = -100  # 近一年内有 降职/降级、免职/撤职/停职
            elif t < 5 and t > 1 and b is True:
                s = -50  # 近1至5年内有 降职/降级、免职/撤职/停职
            elif t >= 5 and b is True:
                s = -20  # 5年前有 降职/降级、免职/撤职/停职
            elif a is True:
                s = -20  # 通报批评、警告、记过
            else:
                s = 0
            punish_field.append(s)
        res = np.min(punish_field)
    else:
        res = 0

    return res

