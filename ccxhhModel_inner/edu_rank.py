
import pandas as pd


# 学校星级映射
def f_sch_star(sch_name,birthY,edu_info):
    if sch_name:
        sch_star = edu_info.ix[edu_info.学校名称.isin([sch_name]), '星级']
        if len(sch_star)!=0:
            sch_star =sch_star.iloc[0]
            if sch_star in [2,3,4]:
                sch_star=2
            elif sch_star in [5,6,7]:
                sch_star=3
        else:
            sch_star=1
    else:
        if int(birthY)<=1978:
            sch_star=4
        else:
            sch_star=5

    return sch_star

# 学校排名映射
def f_sch_rank(sch_name,birthY,edu_info):
    if sch_name:
        sch_rank = edu_info.ix[edu_info.学校名称.isin([sch_name]), '名次']
        if len(sch_rank)!=0:
            sch_rank =sch_rank.iloc[0]
            if sch_rank >=1 & sch_rank<50:
                sch_rank=1
            elif sch_rank >=50 & sch_rank <535:
                sch_rank=2
            else:
                sch_rank=3
        else:
            sch_rank=3
    else:
        if int(birthY)<=1978:
            sch_rank=4
        else:
            sch_rank=5

    return sch_rank

# 学校类型映射

def f_sch_type(sch_name,birthY,edu_info):
    if sch_name:
        sch_type = edu_info.ix[edu_info.学校名称.isin([sch_name]), '院校类型']
        if len(sch_type)!=0:
            sch_type =sch_type.iloc[0]
            if sch_type =='985院校':
                sch_type=1
            elif sch_type == '211院校':
                sch_type=2
            else:
                sch_type=3
        else:
            sch_type=3
    else:
        if int(birthY)<=1978:
            sch_type=4
        else:
            sch_type=5

    return sch_type

def f_edu_degree(edu_degree):
    if pd.notnull(edu_degree):

        if edu_degree[-2:] == '学士':
            res=2
        elif edu_degree[-2:] in ['硕士','博士']:
            res=1
        else:
            res=3
    else:
        res=4
    return res