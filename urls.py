# -*- coding: utf-8 -*-
# @Author  :songtao

import os

from config import *
from handlers import kLine,FundIndex,Price
from handlers.BaseHandler import StaticFileHandler

handlers=[
        (r"/api/kline", kLine.KlineHandler),
        (r"/api/kline_index", kLine.KlineIndexHandler),
        (r"/api/data_name", kLine.DataNameHandler),
        (r"/api/find_index", FundIndex.FindIndexHandler),
        (r"/api/kline1M_index", kLine.Kline1MIndexHandler),
        (r"/api/kline1M", kLine.Kline1MHandler),
        (r"/api/last_price", Price.LastPriceHandler),
    ]
