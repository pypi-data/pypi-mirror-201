# -*- coding: utf-8 -*-
"""
@desc: readme
@author: 1nchaos
@time: 2023/3/29
@log: change log
"""

import time

import pandas as pd

from adata.common.headers import baidu_headers
from adata.common.utils import requests


class StockMarket(object):
    """
    股票行情
    """

    def __init__(self) -> None:
        super().__init__()

    def get_market(self, code: str = '000001', start_date='1990-01-01', k_type=1, adjust_type: int = 1):
        """
        获取当个股票的行情
        :param code: 股票代码
        :param start_date: 开始时间
        :param k_type: k线类型：1.日；2.周；3.月 默认：1 日k
        :param adjust_type: k线复权类型：0.不复权；1.前复权；2.后复权 默认：1 前复权
        :return: k线行情数据
        """
        return self.__market_baidu(code, start_date, k_type, adjust_type)

    def __market_baidu(self, code, start_date, k_type, adjust_type):
        """
        获取百度的股票行情数据
        web： https://gushitong.baidu.com/stock/ab-002926
        url： https://finance.pae.baidu.com/selfselect/getstockquotation?all=1&isIndex=false&isBk=false&isBlock=false&isFutures=false&isStock=true&newFormat=1&group=quotation_kline_ab&finClientType=pc&code=002926&start_time=2018-02-05 00:00:00&ktype=1
        "时间戳", "时间","开盘","收盘","成交量","最高","最低","成交额","涨跌额","涨跌幅","换手率","昨收",
        "ma5均价","ma5成交量","ma10均价","ma10成交量","ma20均价","ma20成交量"
        :param code: 6位股票代码
        :param start_date: 开始时间
        :param k_type: k线类型：1.日；2.周；3.月
        :param adjust_type: k线复权类型：0.不复权；1.前复权；2.后复权 默认：1 前复权 TODO
        :return: k线行情数据
        """
        # 1. 请求接口 url
        api_url = f"https://finance.pae.baidu.com/selfselect/getstockquotation?all=1&isIndex=false&isBk=false&" \
                  f"isBlock=false&isFutures=false&isStock=true&newFormat=1&group=quotation_kline_ab&finClientType=pc&" \
                  f"code={code}&start_time={start_date} 00:00:00&ktype={k_type}"

        res_json = None
        for i in range(3):
            res = requests.request('get', api_url, headers=baidu_headers.json_headers, proxies={})
            # 2. 校验请求结果数据
            res_json = res.json()
            if res_json['ResultCode'] == '0':
                break
            time.sleep(2)
        # 3.解析数据
        # 3.1 空数据时返回为空
        result = res_json['Result']
        if not result:
            return pd.DataFrame()

        # 3.2. 正常解析数据
        keys = res_json['Result']['newMarketData']['keys']
        market_data = res_json['Result']['newMarketData']['marketData']
        market_data_list = str(market_data).split(';')
        data = []
        for one in market_data_list:
            data.append(one.split(','))

        # 4. 封装数据
        result_df = pd.DataFrame(data=data, columns=keys)
        return result_df[['time', 'open', 'close', 'volume', 'high', 'low', 'amount', 'range', 'ratio',
                          'turnoverratio', 'preClose']]


if __name__ == '__main__':
    print(StockMarket().get_market(code='000001', start_date='2021-01-01', k_type=1))
