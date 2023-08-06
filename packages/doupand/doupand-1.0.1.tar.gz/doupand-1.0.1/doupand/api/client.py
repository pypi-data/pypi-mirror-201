# -*-coding: utf-8 -*-
# @Time    : 2023/4/7 01:32
# @Description  : API数据接口

import json
import os
import requests
import time
import pandas as pd
from functools import partial
from doupand.utils import userauth
from doupand.utils import cons as ct

__all__ = ['datareader']


class DataReader:
    __token = ''
    __http_url = ''
    __distribution_url = 'http://api.doupand.com'

    def __init__(self, token='', timeout=15):
        """
        :param token: API的TOKEN，用于用户认证
        :param timeout:
        """
        self.__token = token
        self.__timeout = timeout
        self.__url_expire_time = int(time.time())

    @property
    def __query_token(self):
        """请求口令token"""
        if self.__token == '' or self.__token is None:
            token = userauth.get_token()
            if token is not None and token != '':
                self.__token = token
            else:
                raise Exception('DataReader Init Error!')

        return self.__token

    @property
    def __query_url(self):
        """请求URL"""
        cur_time = int(time.time())
        if self.__http_url and cur_time < self.__url_expire_time:
            return self.__http_url
        else:
            project_dir = os.path.dirname(__file__)
            fp = os.path.join(project_dir, ct.URL_F_P)

            if os.path.exists(fp):
                df = pd.read_csv(fp)
                if cur_time < int(df.loc[0]['expire_time']):
                    self.__url_expire_time = int(df.loc[0]['expire_time'])
                    return str(df.loc[0]['http_url'])

            res = requests.get(self.__distribution_url, timeout=10, headers={'Connection': 'close'})
            result = res.json()
            if result['status'] == "success":
                self.__http_url = res.json()['result']
                self.__url_expire_time = cur_time + 12 * 60 * 60
                df = pd.DataFrame([[self.__http_url, self.__url_expire_time]], columns=['http_url', 'expire_time'])
                df.to_csv(fp, index=False)
                return self.__http_url
            else:
                raise Exception("初始化请求失败，请重试！")

    def query(self, api_name, fields='', **kwargs):
        """
        请求API
        :param api_name: API名称
        :param fields: 返回字段
        :param kwargs: 参数
        :return:
        """
        req_params = {
            'api_name': api_name,
            'token': self.__query_token,
            'params': kwargs,
            'fields': fields
        }

        res = requests.post(self.__query_url, json=req_params, timeout=self.__timeout, headers={'Connection': 'close'})
        result = json.loads(res.text)
        if result['code'] != 0:
            raise Exception(result['msg'])
        data = result['data']
        columns = data['columns']
        values = data['values']

        return pd.DataFrame(values, columns=columns)

    def __getattr__(self, name):
        """
        直接将属性名称作为api_name传入query方法
        :param name:
        :return:
        """
        return partial(self.query, name)


datareader = DataReader()
