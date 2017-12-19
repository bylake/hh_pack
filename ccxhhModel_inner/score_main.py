from ccxhhModel_inner.base_score_hh import base_score
from ccxhhModel_inner.Hh_apply_score_to_inner import *
from ccxhhModel_inner.Hh_amount_score_to_inner import *
from ccxhhModel_inner.log import ABS_log
import pandas as pd


@ABS_log('ccxhh')
def score_main(json_data):
    base_hh = base_score(json_data)  # 计算基准分
    base_hh = int(base_hh)

    ##### 第三方征信分
    sal_score = LvYue(json_data['sal_score'])  # 履约能力评分
    risk_raw = json_data['risk_score'] if pd.notnull(json_data['risk_score']) else 0  # 风险评分
    if risk_raw <= 30:
        risk_score = -risk_raw * 3
    elif risk_raw > 30 and risk_raw <= 60:
        risk_score = -risk_raw * 4
    elif risk_raw > 60:
        risk_score = -risk_raw * 5
    else:
        risk_score = 0

    mul_apply_score = many_apply(json_data['mul_apply_score'])  # 多重申请评分
    black_score = json_data['black_score']
    if pd.notnull(black_score):
        black_score = public_score(json_data['black_score'])  # 公共治安评分
    else:
        black_score = 0

    #### 海航内部字段计算的分数

    marry_score = marry(json_data['marry_status'])  # 婚姻分
    # manage_score = Manage_level(json_data['admin_lvl'])  # 管理级别分
    job_score = job_time(json_data['job_time'])  # 工作年限分
    work_form_score = work_form(json_data['work_form'])  # 用工形式
    company_score = company_time(json_data['corp_time'])  # 进入集团年限
    punish_score = punish(json_data['cnt_0'])  # 惩罚次数
    punish_score_type = punish_types(json_data['punish_type'])
    score = base_hh + sal_score + risk_score + mul_apply_score + black_score + marry_score + \
            job_score + work_form_score + company_score + punish_score + punish_score_type
    # print(base_hh, sal_score, risk_score, mul_apply_score, black_score, marry_score, job_score, work_form_score,
    #       company_score,punish_score,punish_score_type)
    score = int(score)
    if score<=300:
        score = 300
    elif score>900:
        score=900

    ##################################################################  额度分

    score_rank = ((score - 300) / 600) * 100  # 将申请分映射到0-100分
    score_manage = rank(json_data['admin_lvl'])  # 管理级别分
    score_reward = reward(json_data['cnt_1'])  # 奖励次数
    score_reg_time = register(json_data['reg_time'])  # 注册时长
    score_reg_lvl = stage_h(json_data['plat_lvl'])  # 注册等级

    score_amt = int(
        score_rank * 0.6 + 0.2 * score_manage + 0.03 * score_reward + 0.02 * score_reg_lvl + 0.15 * score_reg_time)
    sal_get = sal_get_api(json_data['sal_score'])
    if pd.notnull(sal_get):  # 如果查到收入履约
        final_amt = sal_get * dept_many_apply(json_data['mul_apply_score']) * 12 * coef_tf(score_amt)
        flag_sal = '查到收入履约'
    else:
        edu_sal = sal_edu_degree(json_data['edu_degree']) * 0.2  # 学历预估
        corp_sal = sal_corp_time(json_data['corp_time']) * 0.2  # 集团时间预估
        mana_sal = sal_manage(json_data['admin_lvl']) * 0.5  # 管理级别预估
        city_sal = sal_city(json_data['city_job']) * 0.1
        sal_est = 10000 * (edu_sal + corp_sal + mana_sal + city_sal)  # 收入预估
        final_amt = sal_est * dept_many_apply(json_data['mul_apply_score']) * 12 * coef_tf(score_amt)
        flag_sal = '未查到收入履约'
    return base_hh, score, score_amt, int(final_amt),flag_sal
