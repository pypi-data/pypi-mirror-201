# -*- coding: utf-8 -*-
"""
@desc: readme
@author: 1nchaos
@time: 2023/3/29
@log: change log
"""

import pandas as pd

from adata.common.headers import baidu_headers
from adata.common.utils import requests


class StockDividend(object):
    """
    股票分红
    """

    def __init__(self) -> None:
        super().__init__()

    def get_dividend(self, code='000001'):
        """
        获取当个股票的分红信息
        :param code: 股票代码
        :return: 股票分红信息
        """
        return self.__dividend_baidu(code)

    def __dividend_baidu(self, code):
        """
        获取百度的股票分红数据：公告日；分红方案；除权除息日
        web： https://gushitong.baidu.com/stock/ab-300033
        url： https://gushitong.baidu.com/opendata?openapi=1&dspName=iphone&tn=tangram&client=app&query=300033&code=300033&word=300033&resource_id=5429&ma_ver=4&finClientType=pc
        :param code: 6位股票代码
        :return: 股票分红信息
        """
        # 1.请求接口 url
        api_url = f"https://gushitong.baidu.com/opendata?openapi=1&dspName=iphone&tn=tangram&client=app&" \
                  f"query={code}&code={code}&word={code}&resource_id=5429&ma_ver=4&finClientType=pc"
        res = requests.request('get', api_url, headers=baidu_headers.text_headers)

        # 2. 判断结果是否正确
        if len(res.text) < 1 or res.status_code != 200:
            return pd.DataFrame()
        res_json = res.json()
        if res_json['ResultCode'] != '0':
            return pd.DataFrame()
        # 3.解析数据
        # 3.1 空数据时返回为空
        result = res_json['Result']
        if not result:
            return pd.DataFrame()

        # 3.2 正常解析数据 basicInfo,shareholderEquity,organRating,executiveInfo,bonusTransfer
        new_company = result[-1]['DisplayData']['resultData']['tplData']['result']['tabs'][-1]['content'][
            'newCompany']
        bonus_transfer = new_company['bonusTransfer']
        header = bonus_transfer['header']
        body = bonus_transfer['body']

        # 4. 封装数据
        result_df = pd.DataFrame(data=body, columns=header)
        return result_df[['公告日', '分红方案', '除权除息日']]


if __name__ == '__main__':
    print(StockDividend().get_dividend(code='000001'))
