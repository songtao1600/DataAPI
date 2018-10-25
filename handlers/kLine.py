# -*- coding: utf-8 -*-
# @Author  :songtao

import logging
import datetime

from utils.response_code import RET
from .BaseHandler import BaseHandler

class KlineIndexHandler(BaseHandler):
    """
    kline 数据
    """
    def get(self, *args, **kwargs):

        try:
            cur = self.db.cursor()
        except Exception as e:
            logging.error("创建游标失败", e)
            return self.write(dict(code=RET.DATAERR, errmsg=e))

        sql = f'select source, currency, CAST(amount AS CHAR(50)) as amount,CAST(close_ AS CHAR(50)) as close_,' \
              f'CAST(high_ AS CHAR(50)) as high_,CAST(low_ AS CHAR(50)) as low_,' \
              f'CAST(open_ AS CHAR(50)) as open_, CAST(volume AS CHAR(50)) as volume,' \
              f'DATE_FORMAT(sample_time,"%Y-%m-%d %H:%i:%S") as sample_time   ' \
              f'from kline_data_5m'
        try:
            print(sql)
            cur.execute(sql)
            ret = cur.fetchall()
            cur.close()
            self.write(dict(code=RET.OK,errmsg="", data=ret))
        except Exception as e:
            print(e)
            logging.error("查询数据库错误")
            cur.close()
            return self.write(dict(code=RET.DATAERR, errmsg=e))

class KlineHandler(BaseHandler):
    """
    kline 数据
    """
    def get(self, *args, **kwargs):

        #获取参数
        time_flag = self.get_argument("time_flag", default=None)
        begin_date = self.get_argument("begin_date",default=None)
        end_date = self.get_argument("end_date",default=None)
        source = self.get_argument("source",default=None)
        currency = self.get_argument("currency",default=None)
        info = f'time_flag:{time_flag},source:{source},currency:{currency}, begin_date:{begin_date}, end_date:{end_date}'
        logging.info(info)

        if time_flag == None and begin_date == None and end_date == None and source == None and currency == None:
            self.redirect('/api/kline_index')

        if (begin_date == None and end_date != None) or (begin_date != None and end_date == None):
            return self.write(dict(errcode=RET.PARAMERR, errmsg="参数错误"))

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

        if begin_date: #自定义事件
            sql = f' and sample_time >=\"{begin_date}\" and sample_time <=\"{end_date}\"'
            sql_str = sql_str + sql
        else:  #固定时间
            now = datetime.datetime.now()
            # now = datetime.datetime.now().strftime('%Y-%m-%d')
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
        logging.info('sql_str: %s'% sql_str)
        try:
            cur = self.db.cursor()
        except Exception as e:
            logging.error("创建游标失败",e)
            return self.write(dict(code=RET.DATAERR, errmsg=e))

        # sql = f'select source, currency, CAST(amount AS CHAR(50)) as amount,CAST(close_ AS CHAR(50)) as close_,' \
        #       f'CAST(high_ AS CHAR(50)) as high_,CAST(low_ AS CHAR(50)) as low_,' \
        #       f'CAST(open_ AS CHAR(50)) as open_, CAST(volume AS CHAR(50)) as volume,' \
        #       f'DATE_FORMAT(sample_time,"%Y-%m-%d %H:%i:%S") as sample_time   ' \
        #       f'from kline_data_5m where currency = \"{currency}\" and sample_time >=\"{begin_date}\" and sample_time <=\"{end_date}\"'
        try:
            print(sql_str)
            cur.execute(sql_str)
            ret = cur.fetchall()
            cur.close()
            self.write(dict(code=RET.OK,errmsg="", data=ret))
        except Exception as e:
            print(e)
            logging.error("查询数据库错误")
            cur.close()
            return self.write(dict(code=RET.DATAERR, errmsg=e))

class DataNameHandler(BaseHandler):
    """
    kline 数据
    """
    def get(self, *args, **kwargs):

        try:
            cur = self.db.cursor()
        except Exception as e:
            logging.error("创建游标失败",e)
            return self.write(dict(code=RET.DATAERR, errmsg=e))

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
            self.write(dict(code=RET.OK,errmsg="", data=ret_dict))
        except Exception as e:
            logging.error("查询数据库错误")
            cur.close()
            return self.write(dict(code=RET.DATAERR, errmsg=e))

class Kline1MIndexHandler(BaseHandler):
    """
    kline 数据
    """
    def get(self, *args, **kwargs):

        try:
            cur = self.db.cursor()
        except Exception as e:
            logging.error("创建游标失败", e)
            return self.write(dict(code=RET.DATAERR, errmsg=e))

        try:
            sql = f'select symbol, source, channel, sample_time,CAST(open_ AS CHAR(50)) as open_,' \
              f'CAST(high_ AS CHAR(50)) as high_,CAST(low_ AS CHAR(50)) as low_,' \
              f'CAST(close_ AS CHAR(50)) as close_, CAST(volume AS CHAR(50)) as volume,CAST(coin_volume AS CHAR(50)) as coin_volume,' \
              f'DATE_FORMAT(update_time,"%Y-%m-%d %H:%i:%S") as update_time   ' \
              f'from kline_data_1m order by sample_time desc'
            print(sql)
            cur.execute(sql)
            ret = cur.fetchall()
            cur.close()
            self.write(dict(code=RET.OK,errmsg="", data=ret))
        except Exception as e:
            print(e)
            logging.error("查询数据库错误")
            cur.close()
            return self.write(dict(code=RET.DATAERR, errmsg=e))

class Kline1MHandler(BaseHandler):
    """
    kline 数据
    """

    def get(self, *args, **kwargs):

        print('aaaaaa')
        # 获取参数
        begin_date = self.get_argument("start_time", default=None)
        end_date = self.get_argument("end_time", default=None)
        source = self.get_argument("exchange",default=None)
        trade_currency = self.get_argument("trade_currency",default=None)
        base_currency = self.get_argument("base_currency",default=None)
        period = self.get_argument("period",default=None)
        size = self.get_argument("size",default=None)
        currency = None
        if trade_currency != None and base_currency != None:
            currency = trade_currency + '/' + base_currency
        print(begin_date, end_date, source, currency, period, size)

        sql_str = f'select symbol, source, channel, sample_time,CAST(open_ AS CHAR(50)) as open_,' \
                    f'CAST(high_ AS CHAR(50)) as high_,CAST(low_ AS CHAR(50)) as low_,' \
                    f'CAST(close_ AS CHAR(50)) as close_, CAST(volume AS CHAR(50)) as volume,CAST(coin_volume AS CHAR(50)) as coin_volume,' \
                    f'DATE_FORMAT(update_time,"%Y-%m-%d %H:%i:%S") as update_time   ' \
                    f'from kline_data_1m  where 1=1'

        if begin_date:  # 自定义事件
            sql = f' and sample_time >=\"{begin_date}\"'
            sql_str = sql_str + sql

        if end_date:
            sql = f' and sample_time <=\"{end_date}\"'
            sql_str = sql_str + sql

        if source:
            sql = f' and source =\"{source}\"'
            sql_str = sql_str + sql

        if currency:
            sql = f' and symbol =\"{currency}\"'
            sql_str = sql_str + sql

        sql = ' order by sample_time desc'
        sql_str = sql_str + sql

        if size:
            sql = f' limit {size}'
            sql_str = sql_str + sql

        print(sql_str)
        logging.info('sql_str: %s' % sql_str)
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

    def post(self, *args, **kwargs):

        #获取参数
        symbol = self.get_argument("symbol", default=None)
        channel = self.get_argument("channel",default=None)
        sample_time = self.get_argument("sample_time",default=None)
        open_ = self.get_argument("open_",default=None)
        high_ = self.get_argument("high_",default=None)
        low_ = self.get_argument("low_",default=None)
        close_ = self.get_argument("close_",default=None)
        volume = self.get_argument("volume",default=None)
        coin_volume = self.get_argument("coin_volume",default=None)
        source = self.get_argument("source",default=None)



        try:
            cur = self.db.cursor()
        except Exception as e:
            logging.error("创建游标失败",e)
            return self.write(dict(code=RET.DATAERR, errmsg=e))

        # sql = f'select source, currency, CAST(amount AS CHAR(50)) as amount,CAST(close_ AS CHAR(50)) as close_,' \
        #       f'CAST(high_ AS CHAR(50)) as high_,CAST(low_ AS CHAR(50)) as low_,' \
        #       f'CAST(open_ AS CHAR(50)) as open_, CAST(volume AS CHAR(50)) as volume,' \
        #       f'DATE_FORMAT(sample_time,"%Y-%m-%d %H:%i:%S") as sample_time   ' \
        #       f'from kline_data_5m where currency = \"{currency}\" and sample_time >=\"{begin_date}\" and sample_time <=\"{end_date}\"'
        try:
            str_sql = f'select count(1) as count from kline_data_1m where symbol = \"{symbol}\" and source = \"{source}\" and sample_time = {sample_time}'
            cur.execute(str_sql)
            ret = cur.fetchall()[0]
            count = ret['count']
            if count > 0:
                str_sql=f'update kline_data_1m set open_ = {open_}, high_ = {high_}, low_ = {low_}, close_ = {close_}, volume = {volume}, coin_volume = {coin_volume}' \
                        f' where symbol = \"{symbol}\" and source = \"{source}\" and sample_time = {sample_time}'
            else:
                str_sql = f'insert into kline_data_1m (symbol, source, channel, sample_time, open_, high_, low_, close_, volume, coin_volume) values ' \
                        f'(\"{symbol}\", \"{source}\", \"{channel}\",{sample_time},{open_},{high_},{low_},{close_},{volume},{coin_volume})'
            print(str_sql)
            cur.execute(str_sql)
            cur.close()
            self.write(dict(code=RET.OK,errmsg=""))
        except Exception as e:
            print(e)
            logging.error("查询数据库错误")
            cur.close()
            return self.write(dict(code=RET.DATAERR, errmsg=e))


