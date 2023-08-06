# -*-coding: utf-8 -*-
# @Time    : 2023/4/7 01:32
# @Description  : API数据接口

import pandas as pd
import json
from functools import partial
from doupand.utils import userauth
import requests

__all__ = ['datareader']


class DataReader:
    __token = ''
    __http_url = 'http://api.doupand.com'

    def __init__(self, token='', timeout=15):
        """
        :param token: API的TOKEN，用于用户认证
        :param timeout:
        """
        self.__token = token
        self.__timeout = timeout

    def set_token(self):
        """从本地获取并设置token"""
        token = userauth.get_token()

        if token is not None and token != '':
            self.__token = token
        else:
            raise Exception('DataReader Init Error!')

    def query(self, api_name, fields='', **kwargs):
        """
        请求API
        :param api_name: API名称
        :param fields: 返回字段
        :param kwargs: 参数
        :return:
        """
        if self.__token == '' or self.__token is None:
            self.set_token()

        req_params = {
            'api_name': api_name,
            'token': self.__token,
            'params': kwargs,
            'fields': fields
        }

        res = requests.post(self.__http_url, json=req_params, timeout=self.__timeout, headers={'Connection': 'close'})
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
