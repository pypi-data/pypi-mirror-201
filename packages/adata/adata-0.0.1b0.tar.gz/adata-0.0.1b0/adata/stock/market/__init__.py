# -*- coding: utf-8 -*-
"""
@desc: readme
@author: 1nchaos
@time: 2023/3/29
@log: change log
"""
from .stock_dividend import StockDividend
from .stock_market import StockMarket
from .stock_market_gn import StockMarketGn


class Market(StockMarket, StockMarketGn, StockDividend):

    def __init__(self) -> None:
        super().__init__()


market = Market()
