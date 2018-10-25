# -*- coding: utf-8 -*-
# @Time    :2018/6/14
# @Author  :songtao

import os
import pymysql.cursors

BASEPATH = os.path.dirname(__file__)

SESSION_EXPIRES_SECONDS = 72000 #session失效时间
#Appliaction 配置
settings = {
    'static_path':os.path.join(os.path.dirname(__file__), 'static'),
    'template_path':os.path.join(os.path.dirname(__file__), 'template'),
    'cookie_secret':'ssdsdfdsiwaeijsdcnjiucdsfjkk',
    'xsrf_cookies':False,
    'debug':False,
}

#mysql配置
#mysql_options = {
#    'host':'192.168.1.64',
#    'database':'trade_data',
#    'user':'root',
#    'password':'123456',
#    'charset':'utf8',
#    'port': 3306,
#    'cursorclass': pymysql.cursors.DictCursor
#}

mysql_options = {
    'database': 'trade_data',
    'user': 'bitup',
    'host': '47.75.134.91',
    'password': 'Ne88t9g7uSWVd]b',
    'port': 4423,
    'charset':'utf8',
    'cursorclass': pymysql.cursors.DictCursor,
    'autocommit': True
}


#mysql_options = {
#    'database': 'bitup_sys',
#    'user': 'bitup',
#    'host': '172.31.1.76',
#    'password': 'Up=8u5e3W4Rjhfy8U4',
#    'port': 4423,
#    'charset':'utf8',
#    'cursorclass': pymysql.cursors.DictCursor,
#    'autocommit': True
#}
#redis配置
redis_options = {
    'host':'127.0.0.1',
    'port':6379,
    'socket_timeout':3
}

log_level = 'info'
log_file = os.path.join(os.path.dirname(__file__), 'logs/log')
