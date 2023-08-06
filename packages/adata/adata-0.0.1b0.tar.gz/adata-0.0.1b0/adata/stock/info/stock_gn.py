# -*- coding: utf-8 -*-
"""
@summary: 股票概念
同花顺概念更及时和完整，所以目前暂只基于同花顺的股票概念抓取
@author: 1nchaos
@date: 2023/3/30 16:17
"""
import pandas as pd
from bs4 import BeautifulSoup

from adata.common.headers import ths_headers
from adata.common.utils import requests


class StockGn(object):
    """
    股票概念
    """

    def __init__(self) -> None:
        super().__init__()

    def all_gn_code_ths(self):
        """
        获取同花顺概念列表：代码和名称
        :return: 概念[[code,name]]
        """
        return pd.concat([self.gn_code_ths_pc(), self.gn_code_ths_app()]).reset_index(drop=True)

    def gn_code_ths_pc(self):
        """
        获取同花顺的所有概念和概念代码
        web: http://q.10jqka.com.cn/gn/
        """
        # 1. 请求接口 url
        api_url = f"http://q.10jqka.com.cn/gn/"
        for i in range(3):
            res = requests.request('get', api_url, headers=ths_headers.text_headers, proxies={})
            # 2. 判断请求是否正确
            text = res.text
            if res.status_code != 200 or len(text) < 1:
                continue
            # 3. 解析数据
            soup = BeautifulSoup(text, 'html.parser')
            data = []
            for a in soup.find_all('a'):
                href = str(a['href'])
                if href.startswith(api_url + 'detail/code/'):
                    data.append([href[-7: -1], a.string, href])

            # 4. 封装数据
            return pd.DataFrame(data=data, columns=['code', 'name', 'href'])[['code', 'name']]

    def gn_code_ths_app(self):
        """
        获取app的概率列表，通过问财询问得到结果
        :return: app的概念列表： code，name
        """
        data = []
        for i in range(1, 10):
            api_url = f"http://search.10jqka.com.cn/gateway/urp/v7/landing/getDataList?perpage=100&page={i}&query=%E6%89%80%E6%9C%89%E6%A6%82%E5%BF%B5&condition=%5B%7B%22indexName%22%3A%22%E6%8C%87%E6%95%B0%40%E5%90%8C%E8%8A%B1%E9%A1%BA%E6%A6%82%E5%BF%B5%E6%8C%87%E6%95%B0%22%2C%22indexProperties%22%3A%5B%5D%2C%22source%22%3A%22new_parser%22%2C%22type%22%3A%22index%22%2C%22indexPropertiesMap%22%3A%7B%7D%2C%22reportType%22%3A%22null%22%2C%22chunkedResult%22%3A%22%E6%89%80%E6%9C%89%E6%A6%82%E5%BF%B5%22%2C%22valueType%22%3A%22_%E6%8C%87%E6%95%B0%E7%B1%BB%E5%9E%8B%22%2C%22domain%22%3A%22abs_a%E6%8C%87%E9%A2%86%E5%9F%9F%22%2C%22uiText%22%3A%22%E5%90%8C%E8%8A%B1%E9%A1%BA%E6%A6%82%E5%BF%B5%E6%8C%87%E6%95%B0%22%2C%22sonSize%22%3A0%2C%22queryText%22%3A%22%E5%90%8C%E8%8A%B1%E9%A1%BA%E6%A6%82%E5%BF%B5%E6%8C%87%E6%95%B0%22%2C%22relatedSize%22%3A0%7D%5D&urp_sort_index=%E6%8C%87%E6%95%B0%E4%BB%A3%E7%A0%81&source=Ths_iwencai_Xuangu&urp_sort_way=desc&codelist=&page_id=&logid=35df00ee5ae706d0dfcd0dbfdb846e0c&ret=json_all&sessionid=35df00ee5ae706d0dfcd0dbfdb846e0c&iwc_token=0ac9667016801698001765831&user_id=Ths_iwencai_Xuangu_7fahywzhbkrh4lwwkwfw936njqbjzsly&uuids%5B0%5D=23119&query_type=zhishu&comp_id=6367801&business_cat=soniu&uuid=23119"
            res = requests.request('get', url=api_url, headers=ths_headers.c_headers)
            res_json = res.json()
            if res_json['status_msg'] == 'ok':
                data_list = res_json['answer']['components'][0]['data']['datas']
                if len(data_list) < 1:
                    break
                for d in data_list:
                    data.append([d['code'], d['指数简称']])
        return pd.DataFrame(data=data, columns=['code', 'name']).drop_duplicates(keep='first', inplace=False,
                                                                                 ignore_index=False)


if __name__ == '__main__':
    print(StockGn().all_gn_code_ths())
    print(StockGn().gn_code_ths_pc())
    print(StockGn().gn_code_ths_app())
