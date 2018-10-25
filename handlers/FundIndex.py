# -*- coding:utf-8 -*-
# @Author :songtao
import logging
import datetime

from utils.response_code import RET
from .BaseHandler import BaseHandler

class FindIndexHandler(BaseHandler):
    """
    kline 数据
    """
    def get(self, *args, **kwargs):

        #获取参数
        begin_date = self.get_argument("begin_date",default=None)
        end_date = self.get_argument("end_date",default=None)
        source = self.get_argument("source",default=None)
        currency = self.get_argument("currency",default=None)
        info = f'source:{source},currency:{currency}, begin_date:{begin_date}, end_date:{end_date}'
        logging.info(info)
        print(begin_date, end_date, source, currency)
        sql_str = f'select DATE_FORMAT(sample_time,"%Y-%m-%d %H:%i:%S") as sample_time, CAST(value AS CHAR(50)) as value from fund_index_raw_dynamic_data where 1=1'

        if begin_date == None and end_date == None and source == None and currency == None:
            try:
                cur = self.db.cursor()
                cur.execute(sql_str)
                ret = cur.fetchall()
                cur.close()
                self.write(dict(code=RET.OK, errmsg="", data=ret))
            except Exception as e:
                print(e)
                logging.error("查询数据库错误")
                cur.close()
                return self.write(dict(code=RET.DATAERR, errmsg=e))

        if (begin_date == None and end_date != None) or (begin_date != None and end_date == None):
            return self.write(dict(errcode=RET.PARAMERR, errmsg="参数错误"))

        # sql_str = f'select value from kline_data_5m where 1=1'

        if source == None or currency == None:
            return self.write(dict(errcode=RET.PARAMERR, errmsg="参数错误"))

        name = source + '@' + currency

        sql = f' and name =\"{name}\"'
        sql_str = sql_str + sql

        if begin_date: #自定义时间
            sql = f' and sample_time >=\"{begin_date}\" and sample_time <=\"{end_date}\"'
            sql_str = sql_str + sql

        logging.info('sql_str: %s'% sql_str)
        print(sql_str)
        try:
            cur = self.db.cursor()
        except Exception as e:
            print(e)
            logging.error("创建游标失败",e)

        try:
            cur.execute(sql_str)
            ret = cur.fetchall()
            cur.close()
            self.write(dict(code=RET.OK,errmsg="", data=ret))
        except Exception as e:
            print(e)
            logging.error("查询数据库错误")
            cur.close()
            return self.write(dict(code=RET.DATAERR, errmsg=e))
