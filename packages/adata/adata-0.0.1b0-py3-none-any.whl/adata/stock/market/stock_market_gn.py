# -*- coding: utf-8 -*-
"""
@summary: 股票概念 行情
同花顺概念更及时和完整，所以目前暂只基于同花顺的股票概念抓取,网页数据中心和手机概念板块
http://d.10jqka.com.cn/v6/line/48_885772/01/last1800.js
http://search.10jqka.com.cn/gateway/urp/v7/landing/getDataList?query=%E6%89%80%E6%9C%89%E6%A6%82%E5%BF%B5&condition=%5B%7B%22indexName%22%3A%22%E6%8C%87%E6%95%B0%40%E5%90%8C%E8%8A%B1%E9%A1%BA%E6%A6%82%E5%BF%B5%E6%8C%87%E6%95%B0%22%2C%22indexProperties%22%3A%5B%5D%2C%22source%22%3A%22new_parser%22%2C%22type%22%3A%22index%22%2C%22indexPropertiesMap%22%3A%7B%7D%2C%22reportType%22%3A%22null%22%2C%22chunkedResult%22%3A%22%E6%89%80%E6%9C%89%E6%A6%82%E5%BF%B5%22%2C%22valueType%22%3A%22_%E6%8C%87%E6%95%B0%E7%B1%BB%E5%9E%8B%22%2C%22domain%22%3A%22abs_a%E6%8C%87%E9%A2%86%E5%9F%9F%22%2C%22uiText%22%3A%22%E5%90%8C%E8%8A%B1%E9%A1%BA%E6%A6%82%E5%BF%B5%E6%8C%87%E6%95%B0%22%2C%22sonSize%22%3A0%2C%22queryText%22%3A%22%E5%90%8C%E8%8A%B1%E9%A1%BA%E6%A6%82%E5%BF%B5%E6%8C%87%E6%95%B0%22%2C%22relatedSize%22%3A0%7D%5D&urp_sort_index=%E6%8C%87%E6%95%B0%E4%BB%A3%E7%A0%81&source=Ths_iwencai_Xuangu&perpage=500&page=1&urp_sort_way=desc&codelist=&page_id=&logid=35df00ee5ae706d0dfcd0dbfdb846e0c&ret=json_all&sessionid=35df00ee5ae706d0dfcd0dbfdb846e0c&iwc_token=0ac9667016801698001765831&user_id=Ths_iwencai_Xuangu_7fahywzhbkrh4lwwkwfw936njqbjzsly&uuids%5B0%5D=23119&query_type=zhishu&comp_id=6367801&business_cat=soniu&uuid=23119
885772 表示手机端的概念代码
@author: 1nchaos
@date: 2023/3/30 16:17
"""
import copy
import json

import pandas as pd

from adata.common.headers import ths_headers
from adata.common.utils import requests


class StockMarketGn(object):
    """
    股票概念 行情
    """

    def __init__(self) -> None:
        super().__init__()

    def get_market_gn_ths(self, code: str = '886013', k_type: int = 1, adjust_type: int = 1):
        """
        获取同花顺的概率的行情
        web: http://q.10jqka.com.cn/gn/
        url: http://d.10jqka.com.cn/v6/line/48_886013/01/last1800.js
        00 日k不复权；01日k前复权；02日k后复权；11周k前复权；21月k前复权
        :param code: 同花顺概念代码
        :param k_type: k线类型：1.日；2.周；3.月 默认：1 日k
        :param adjust_type: k线复权类型：0.不复权；1.前复权；2.后复权 默认：1 前复权
        :return: k线行情数据 [日期，开，高，低，收,成交量，成交额]
        成交量：股 820953530  821万手
        成交额：元 16959251000.000 169.6亿
        """
        # 1.接口 url
        api_url = f"http://d.10jqka.com.cn/v6/line/48_{code}/{adjust_type}{k_type}/last1800.js"
        headers = copy.deepcopy(ths_headers.c_headers)
        headers['Host'] = 'd.10jqka.com.cn'
        res = requests.request('get', api_url, headers=headers, proxies={})
        text = res.text
        result_text = text[text.index('{'):-1]
        data_list = json.loads(result_text)['data'].split(';')
        data = []
        for d in data_list:
            data.append(str(d).split(',')[0:7])
        return pd.DataFrame(data=data, columns=['trade_date', 'open', 'high', 'low', 'close', 'vol', 'amount'])

    def get_market_gn_today_ths(self, code):
        """
        获取概念行情当日分时 TODO
        web： http://d.10jqka.com.cn/v6/time/48_886013/last.js
        :param code: 概念代码
        """


if __name__ == '__main__':
    print(StockMarketGn().get_market_gn_ths(code='886013'))
