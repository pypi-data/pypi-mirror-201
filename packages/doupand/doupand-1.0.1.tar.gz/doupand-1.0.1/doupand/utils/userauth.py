# -*-coding: utf-8 -*-
# @Time    : 2023/4/7 00:31
# @Description  : 用户认证

import pandas as pd
import os
from doupand.utils import cons as ct


def set_token(token):
    df = pd.DataFrame([token], columns=['token'])
    # user_home = os.path.expanduser('~')
    project_dir = os.path.dirname(__file__)
    fp = os.path.join(project_dir, ct.TOKEN_F_P)
    df.to_csv(fp, index=False)


def get_token():
    # user_home = os.path.expanduser('~')
    project_dir = os.path.dirname(__file__)
    fp = os.path.join(project_dir, ct.TOKEN_F_P)
    if os.path.exists(fp):
        df = pd.read_csv(fp)
        return str(df.loc[0]['token'])
    else:
        print(ct.TOKEN_ERR_MSG)
        return None
