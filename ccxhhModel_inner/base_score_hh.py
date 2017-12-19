import pandas as pd
from ccxhhModel_inner.edu_rank import *
from ccxhhModel_inner.f_basevar import *
from sklearn.externals import joblib
import pickle
import os
from ccxhhModel_inner.log import ABS_log

with open('school_rank.pkl','rb') as f: edu_info = pickle.load(f) # 读入学历数据
path = os.path.dirname(os.path.realpath(__file__))

@ABS_log('ccxhh')
def base_score(json_data):
    '''
    :param json_data:
    :return: base_score
    '''

    df = pd.DataFrame(index=['id'])
    mob = json_data['mobile']
    cid = json_data['cid']
    birthY = cid[6:10] # 出生年
    df['age'] = f_age(cid) # 年龄
    df['gender'] = f_gender(cid) # 性别
    df['mobile_prov_lvl'] = f_mobile_prov_lvl(f_get_mobile_prov(mob)) #  手机省份等级
    df['mobile_city_lvl'] = f_mobile_city_lvl(f_get_mobile_city(mob)) # 手机城市等级
    df['idno_prov_lvl'] = f_cid_prov_lvl(get_idno_prov(cid)) #  身份证省份等级
    df['idno_city_lvl'] = f_cid_prov_lvl(get_idno_city(cid)) #  身份证城市等级
    df['issame_prov'] = f_2equal_addr(f_get_mobile_prov(mob),get_idno_prov(cid)) # 省份是否一致
    df['issame_city'] = f_2equal_addr(f_get_mobile_city(mob),get_idno_city(cid)) # 城市是否一致

    df['edu_degree'] = json_data['edu_degree'] # 学历等级)
    if pd.isnull(json_data['edu_degree']):
        if birthY<='1978':
            df['edu_degree'] = 4
        else:
            df['edu_degree'] = 5
    df['graduate_Y'] = json_data['graduate_Y'] # 毕业年限
    if pd.isnull(json_data['graduate_Y']): # 如果没有毕业年限数据，则直接按最低值处理
        df['graduate_Y'] = -99
    df['school_star'] = f_sch_star(json_data['top_sch_name'],birthY,edu_info)
    df['school_rank'] = f_sch_rank(json_data['top_sch_name'],birthY,edu_info)
    df['edu_school'] = f_sch_type(json_data['top_sch_name'],birthY,edu_info)

    mob_list = ['mob_3_134', 'mob_3_135', 'mob_3_136', 'mob_3_137', 'mob_3_138',
     'mob_3_139', 'mob_3_147', 'mob_3_150', 'mob_3_151', 'mob_3_152',
     'mob_3_157', 'mob_3_158', 'mob_3_159', 'mob_3_178', 'mob_3_182',
     'mob_3_183', 'mob_3_184', 'mob_3_187', 'mob_3_188']
    mob_var = 'mob_3_' + str(mob)[:3]

    for i in mob_list:
        df[i] = 0
    if mob_var in mob_list:
        df[mob_var]=1



    #### 加载模型
    model_path = os.path.join(path,'haihang_basevar.model')
    xgb_model = joblib.load(model_path)

    #df2['edu_degree']=5
    df3=df[['edu_degree','edu_school','school_star','school_rank','mobile_city_lvl','mobile_prov_lvl',\
            'age','gender','idno_city_lvl','idno_prov_lvl','issame_prov','issame_city','graduate_Y',\
            'mob_3_134','mob_3_135','mob_3_136','mob_3_137','mob_3_138','mob_3_139','mob_3_147',\
            'mob_3_150','mob_3_151','mob_3_152','mob_3_157','mob_3_158','mob_3_159',\
            'mob_3_178','mob_3_182','mob_3_183','mob_3_184','mob_3_187','mob_3_188']]

    odd = list(map(lambda i: i/(1-i),xgb_model.predict_proba(df3)[:,1]))
    score_test = 600-40/np.log(2)*np.log(odd[0])

    return score_test