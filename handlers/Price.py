# -*- coding:utf-8 -*-
# @Author :songtao

import logging
import json

from utils.response_code import RET
from .BaseHandler import BaseHandler
from utils.redis_store import RedisStore


class LastPriceHandler(BaseHandler):
    """
    lastprice 数据
    """

    def get(self, *args, **kwargs):
        # 获取参数
        source = self.get_argument("exchange",default=None)
        trade_currency = self.get_argument("trade_currency",default=None)
        base_currency = self.get_argument("base_currency",default=None)

        try:
            redis = RedisStore()
            key = f'{source}/tick/{trade_currency}{base_currency}'
            data = redis.get(key)
            data = data.decode()
            ret = json.loads(data) 
            self.write(dict(code=RET.OK, errmsg="", data=ret))
        except Exception as e:
            print(e)
            return self.write(dict(code=RET.DATAERR, errmsg=e))

