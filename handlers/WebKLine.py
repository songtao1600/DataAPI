# -*- coding: utf-8 -*-
# @Author  :songtao

import logging
import datetime
import json
from utils.response_code import RET
from .BaseHandler import BaseHandler
from tornado.websocket import WebSocketHandler
from .WebSocketBaseHandler import WebSocketBaseHandler
import pymysql

class wsKlineIndexHandler(WebSocketBaseHandler):
    """
    kline 数据
    """
    def on_message(self, message):

        try:
            cur = self.db.cursor()
        except Exception as e:
            print(e)
            logging.error("创建游标失败", e)
            return self.write_message(json.dumps(dict(code=RET.DATAERR, errmsg=e)))

        sql = f'select source, currency, CAST(amount AS CHAR(50)) as amount,CAST(close_ AS CHAR(50)) as close_,' \
              f'CAST(high_ AS CHAR(50)) as high_,CAST(low_ AS CHAR(50)) as low_,' \
              f'CAST(open_ AS CHAR(50)) as open_, CAST(volume AS CHAR(50)) as volume,' \
              f'DATE_FORMAT(sample_time,"%Y-%m-%d %H:%i:%S") as sample_time   ' \
              f'from kline_data_5m'
        try:
            cur.execute(sql)
            ret = cur.fetchall()
            cur.close()
            self.write_message(json.dumps(dict(code=RET.OK,errmsg="", data=ret)))
        except Exception as e:
            logging.error("查询数据库错误")
            print(e)
            cur.close()
            self.write_message(json.dumps(dict(code=RET.DATAERR, errmsg=e)))

class wsKlineHandler(WebSocketBaseHandler):
    """
    kline 数据
    """
    def on_message(self, message):

        #获取参数
        message = json.loads(message)
        time_flag = message.get('message', None)
        begin_date = message.get('begin_date', None)
        end_date = message.get('end_date', None)
        source = message.get('source', None)
        currency = message.get('currency', None)

        info = f'time_flag:{time_flag},source:{source},currency:{currency}, begin_date:{begin_date}, end_date:{end_date}'
        logging.info(info)
        if time_flag == None and begin_date == None and end_date == None and source == None and currency == None:
            try:
                cur = self.db.cursor()
            except Exception as e:
                logging.error("创建游标失败", e)
                return self.write_message(json.dumps(dict(code=RET.DATAERR, errmsg=e)))

            sql = f'select source, currency, CAST(amount AS CHAR(50)) as amount,CAST(close_ AS CHAR(50)) as close_,' \
                  f'CAST(high_ AS CHAR(50)) as high_,CAST(low_ AS CHAR(50)) as low_,' \
                  f'CAST(open_ AS CHAR(50)) as open_, CAST(volume AS CHAR(50)) as volume,' \
                  f'DATE_FORMAT(sample_time,"%Y-%m-%d %H:%i:%S") as sample_time   ' \
                  f'from kline_data_5m'
            try:
                cur.execute(sql)
                ret = cur.fetchall()
                cur.close()
                self.write_message(json.dumps(dict(code=RET.OK, errmsg="", data=ret)))
            except Exception as e:
                logging.error("查询数据库错误")
                print(e)
                cur.close()
                self.write_message(json.dumps(dict(code=RET.DATAERR, errmsg=e)))

        if (begin_date == None and end_date != None) or (begin_date != None and end_date == None):
            return self.write_message(json.dumps(dict(errcode=RET.PARAMERR, errmsg="参数错误")))

        sql_str = f'select source, currency, CAST(amount AS CHAR(50)) as amount,CAST(close_ AS CHAR(50)) as close_,' \
              f'CAST(high_ AS CHAR(50)) as high_,CAST(low_ AS CHAR(50)) as low_,' \
              f'CAST(open_ AS CHAR(50)) as open_, CAST(volume AS CHAR(50)) as volume,' \
              f'DATE_FORMAT(sample_time,"%Y-%m-%d %H:%i:%S") as sample_time ' \
              f'from kline_data_5m where 1=1'

        if source:
            sql = f' and source =\"{source}\"'
            sql_str = sql_str + sql
        if currency:
            sql = f' and currency =\"{currency}\"'
            sql_str = sql_str + sql

        if begin_date: #自定义时间
            sql = f' and sample_time >=\"{begin_date}\" and sample_time <=\"{end_date}\"'
            sql_str = sql_str + sql
        else:  #固定时间
            now = datetime.datetime.now()
            if time_flag == '1':
                begin_date = (now + datetime.timedelta(days=-1)).strftime('%Y-%m-%d')
                end_date = now.strftime('%Y-%m-%d')
                sql = f' and sample_time >=\"{begin_date}\" and sample_time <=\"{end_date}\"'
                sql_str = sql_str + sql
            elif time_flag == '2':
                begin_date = (now + datetime.timedelta(weeks=-1)).strftime('%Y-%m-%d')
                end_date = now.strftime('%Y-%m-%d')
                sql = f' and sample_time >=\"{begin_date}\" and sample_time <=\"{end_date}\"'
                sql_str = sql_str + sql
            elif time_flag == '3':
                begin_date = (now + datetime.timedelta(days=-30)).strftime('%Y-%m-%d')
                end_date = now.strftime('%Y-%m-%d')
                sql = f' and sample_time >=\"{begin_date}\" and sample_time <=\"{end_date}\"'
                sql_str = sql_str + sql
            elif time_flag == '4':
                begin_date = (now + datetime.timedelta(days=-90)).strftime('%Y-%m-%d')
                end_date = now.strftime('%Y-%m-%d')
                sql = f' and sample_time >=\"{begin_date}\" and sample_time <=\"{end_date}\"'
                sql_str = sql_str + sql
            elif time_flag == '5':
                begin_date = (now + datetime.timedelta(days=-180)).strftime('%Y-%m-%d')
                end_date = now.strftime('%Y-%m-%d')
                sql = f' and sample_time >=\"{begin_date}\" and sample_time <=\"{end_date}\"'
                sql_str = sql_str + sql
            else:
                pass
        print(sql_str)
        logging.info('sql_str: %s'% sql_str)
        try:
            cur = self.db.cursor()
        except Exception as e:
            logging.error("创建游标失败",e)
            return self.write_message(json.dumps(dict(code=RET.DATAERR, errmsg=e)))

        try:
            cur.execute(sql_str)
            ret = cur.fetchall()
            cur.close()
            self.write_message(json.dumps(dict(code=RET.OK,errmsg="", data=ret)))
        except Exception as e:
            logging.error("查询数据库错误")
            cur.close()
            return self.write_message(json.dumps(dict(code=RET.DATAERR, errmsg=e)))

class wsDataNameHandler(WebSocketBaseHandler):
    """
    kline 数据
    """
    def on_message(self, message):

        try:
            cur = self.db.cursor()
        except Exception as e:
            logging.error("创建游标失败",e)
            return self.write_message(json.dumps(dict(code=RET.DATAERR, errmsg=e)))

        ret_dict = {}
        currencys = []
        sources = []
        sql_source = f'select distinct(source) as source from kline_data_5m'
        sql_currency = f'select distinct(currency) as currency from kline_data_5m'
        try:
            cur.execute(sql_source)
            ret1 = cur.fetchall()
            for r1 in ret1:
                for k,v in r1.items():
                    sources.append(v)
            cur.execute(sql_currency)
            ret2 = cur.fetchall()
            for r2 in ret2:
                for k,v in r2.items():
                    currencys.append(v)
            ret_dict['source'] = sources
            ret_dict['currency'] = currencys
            cur.close()
            self.write_message(json.dumps(dict(code=RET.OK, errmsg="", data=ret_dict)))
        except Exception as e:
            logging.error("查询数据库错误")
            cur.close()
            return self.write_message(json.dumps(dict(code=RET.DATAERR, errmsg=e)))

