# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
from f_basevar import *


# # 对内授信额度模型

# # 1，对内申请评分模型分值



# # 2，管理级别  
# 该变量规则权重值为20%

# In[3]:

# 已经将权重计算在内
def rank(x):
    weight = 0.2
    # 管理级别
    if pd.notnull(x):

        if x in ['M16', 'M15', 'M14', 'M13', 'M12', 'M11', 'M10', 'M9', 'M8']:
            rank_hh = 100
        elif x in ['M7', 'M6']:
            rank_hh = 80
        elif x in ['M4', 'M3', 'M5']:
            rank_hh = 40
        else:
            rank_hh = 20
    else:
        rank_hh = 20
    return rank_hh


# # 3.奖励次数
# 该变量规则权重值为5%

# In[48]:

# 已经将权重计算在内
def reward(x):
    weight = 0.03
    # 奖励次数
    if pd.notnull(x):

        if x >= 20:
            reward_hh = 100
        elif x > 10 and x < 20:
            reward_hh = 80
        elif x > 5 and x <= 10:
            reward_hh = 60
        elif x > 2 and x <= 5:
            reward_hh = 40
        elif x > 0 and x <= 2:
            reward_hh = 20
        else:
            reward_hh = 0
    else:
        reward_hh = 0

    return reward_hh


# # 4理财平台注册时长
# 该变量规则权重值为5%

# In[4]:


def register(x):
    weight = 0.02
    # 理财平台注册时长
    if pd.notnull(x):

        if x >= 36:
            reg = 100
        elif x > 12 and x < 36:
            reg = 60
        elif x > 0 and x <= 12:
            reg = 20
        else:
            reg = 0
    else:
        reg = 0

    return reg


# # 5理财平台会员等级
# 该变量规则权重值为5%

# In[5]:

def stage_h(x):
    weight =0.15
    # 理财平台会员等级
    if pd.notnull(x):

        if x == 'JBHCLUB钻石卡会员':
            stage_lvl = 100
        elif x == 'JBHCLUB铂金卡会员':
            stage_lvl = 90
        elif x == 'JBHCLUB金卡会员':
            stage_lvl = 80
        elif x == '优选会员':
            stage_lvl = 50
        elif x == '普通会员':
            stage_lvl = 20
        else:
            stage_lvl = 0
    else:
        stage_lvl = 0

    return stage_lvl


######################  收入预估
### 管理级别预估
def sal_manage(x):
    if pd.notnull(x):

        if x in ['M8', 'M9', 'M10', 'M11', 'M12', 'M13', 'M14', 'M15']:
            return 10
        elif x in ['M5', 'M6', 'M7']:
            return 6
        elif x in ['M3', 'M4']:
            return 4
        else:
            return 2
    else:
        return 2

### 集团时间预估
def sal_corp_time(x):
    if pd.notnull(x):

        if x > 180:
            return 5
        elif (x > 120) & (x <= 180):
            return 3
        elif (x > 60) & (x <= 120):
            return 2
        elif (x > 36) & (x <= 60):
            return 1
        elif (x > 12) & (x <= 36):
            return 0.8
        else:
            return 0.5
    else:
        return 0.5


### 学历预估
def sal_edu_degree(x):
    if pd.notnull(x):

        if x == 1:  # 研究生
            return 5
        elif x == 2:  # 本科生
            return 3
        elif x == 3:  # 专科及其他
            return 1
        else:  # 无学历
            return 0.5
    else:
        return 0.5

def sal_city(x):
    city_lvl = f_dict_city_level(x)
    if city_lvl == 1:
        res = 5
    if city_lvl == 2:
        res = 4
    if city_lvl == 3:
        res = 3
    if city_lvl == 4:
        res = 2
    else:
        res = 1
    return res


def dept_many_apply(x):
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
        if sub_score == 0 and score4 == 0:  # 没命中多头申请
            thres = 0.5
        elif score4 != 0:  # 命中非银多头申请
            thres = 0.2
        elif score4 == 0 and sub_score != 0:  # 命中银行多头申请
            thres = 0.4
    else:
        thres = 0.5

    return thres


################################  授信评分与授信系数的换算
def coef_tf(x):
    '''
    :param 授信评分:
    :return: 授信系数
    '''
    if x >= 0 and x <= 19:
        score = 0.2
    elif x > 19 and x <= 29:
        score = 0.4
    elif x >= 30 and x <= 39:
        score = 0.6
    elif x >= 40 and x < 49:
        score = 0.8
    elif x >= 50 and x < 59:
        score = 1
    elif x >= 60 and x < 69:
        score = 1.2
    elif x >= 70 and x < 84:
        score = 1.8
    elif x >= 85:
        score = 2

    return score


def sal_get_api(x):
    if pd.notnull(x):

        if x > 75:
            return 40000
        elif (x >= 62) & (x <= 75):
            return 30000
        elif (x >= 51) & (x <= 61):
            return 15000
        elif (x >= 44) & (x <= 50):
            return 7500
        else:
            return 4000
    else:
        return np.nan
