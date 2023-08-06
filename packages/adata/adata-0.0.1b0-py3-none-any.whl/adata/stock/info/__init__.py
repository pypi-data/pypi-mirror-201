# -*- coding: utf-8 -*-
"""
@desc: readme
@author: 1nchaos
@time: 2023/3/28
@log: change log
"""
from .stock_code import StockCode
from .stock_gn import StockGn


class Info(StockCode, StockGn):

    def __init__(self) -> None:
        super().__init__()


info = Info()
