# -*- coding: utf-8 -*-
# @Author  :songtao
# @File    :server.py

import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver
from handlers import kLine
import pymysql
import redis

from config import *
from tornado.options import options, define
from urls import handlers

define('port', default=8002, type=int)

class Application(tornado.web.Application):
    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)
        self.db = pymysql.connect(**mysql_options)

def main():
    options.logging = log_level
    options.log_file_prefix = log_file
    tornado.options.parse_command_line()

    app = Application(handlers, **settings)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)

    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()

