# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 16:41:56 2017

@author: chenlw_ZCX
"""
import pandas as pd
import numpy as np
import pickle
import re
import os
from datetime import datetime


#pkg_path = os.path.split(os.path.realpath(__file__))[0]
#dict_path = os.path.join(pkg_path, 'addr_dict')
idno_path = os.path.join('.', 'idno_dict.pkl')
mobile_path = os.path.join('.', 'mobile_addr_dict.pkl')

with open(idno_path, 'rb') as f:
    idno_province = pickle.load(f)
    idno_city = pickle.load(f)

with open(mobile_path, 'rb') as f:
    mobile_addr = pickle.load(f)


def f_age(idno):
    present_year = datetime.today().year
    try:

        if len(idno)==18:
            return present_year - int(idno[6:10])
        elif len(idno)==15:
            return present_year-int('19'+idno[6:8])
        else:
            return np.nan
    except:
        return np.nan


def f_gender(idno):
    '''
    依据身份证计算出性别 1：男  0：女
    :param idno:
    :return:
    '''
    try:
        return int(idno[-2]) % 2
    except:
        return np.nan

def f_dict_prov_level(x):
    pattern_1 = '上海|北京|天津|广东|澳门|香港'
    pattern_2 = '江苏|山东|福建|浙江|安徽'
    pattern_3 = '湖北|湖南|河南|河北|江西|山西|陕西'
    pattern_4 = '广西|海南|云南|四川|贵州|重庆'
    pattern_5 = '黑龙江|吉林|辽宁|内蒙古|甘肃|新疆|青海|宁夏|西藏'
    if re.search(pattern_1, str(x)) is not None:
        return 1
    elif re.search(pattern_2, str(x)) is not None:
        return 2

    elif re.search(pattern_3, str(x)) is not None:
        return 3
    elif re.search(pattern_4, str(x)) is not None:
        return 4
    elif re.search(pattern_5, str(x)) is not None:
        return 5
    else:
        return 6


def f_cid_prov_lvl(idno_prov):
    '''
    获取身份证的省份等级
    :param id_card_address:
    :return:
    '''
    return f_dict_prov_level(idno_prov)


def f_mobile_prov_lvl(mobile_province):
    '''
    获取手机号归属地的省份等级
    :param mobile_province:
    :return:
    '''
    return f_dict_prov_level(mobile_province)

def f_dict_city_level(x):
    pattern_1 = '北京|上海|广州|深圳|天津'  # 一线
    pattern_2 = '杭州|南京|济南|重庆|青岛|大连|宁波|厦门'  # 二线发达
    pattern_3 = '成都|武汉|哈尔滨|沈阳|西安|长春|长沙|福州|郑州|石家庄|苏州|佛山|东莞|无锡|烟台|太原'  # 二线中等发达
    pattern_4 = '合肥|南昌|南宁|昆明|温州|淄博|唐山'  # 二线发展较弱

    if x not in [None, np.nan]:
        if re.search(pattern_1, str(x)) is not None:
            return 1
        elif re.search(pattern_2, str(x)) is not None:
            return 2
        elif re.search(pattern_3, str(x)) is not None:
            return 3
        elif re.search(pattern_4, str(x)) is not None:
            return 4
        else:
            return 5  # 三线以下城市
    else:
        return 6  # 缺失


def f_cid_city_lvl(id_city):
    '''
    身份证地址信息 获取城市，并归约于对应的等级
    :param id_city:
    :return:
    '''
    return f_dict_city_level(id_city)


def f_mobile_city_lvl(mobile_city):
    '''
    手机号归属地 获取城市，并归约于对应的等级
    :param mobile_city:
    :return:
    '''
    return f_dict_city_level(mobile_city)
    
    
def get_mobile_7(x):
    return str(x).strip()[:7]

def f_get_mobile_city(mobile):
    '''
    单次查询
    :param mobile:
    :return:
    '''
    try:
        qy = 'MobileNumber=="{}"'.format(get_mobile_7(mobile))
        return mobile_addr.query(qy).MobileCity.values[0]
    except:
        return np.nan


def f_get_mobile_prov(mobile):
    '''
    单次查询
    :param mobile:
    :return:
    '''
    try:
        qy = 'MobileNumber=="{}"'.format(get_mobile_7(mobile))
        return mobile_addr.query(qy).MobileProv.values[0]
    except:
        return np.nan
        
def get_idno_prov(x):
    try:
        return idno_province[str(x).strip()[:2]]
    except:
        return np.nan


def get_idno_city(x):
    try:
        return idno_city[str(x).strip()[:4]]
    except:
        return np.nan
        
def f_2equal_addr(x, y):
    if x not in [None, np.nan] and y not in [None, np.nan]:
        x = str(x)
        y = str(y)
        if len(x) > len(y):
            return int(re.search(y, x) is not None)
        elif len(x) <= len(y):
            return int(re.search(x, y) is not None)
        else:
            return 0
    else:
        return 0