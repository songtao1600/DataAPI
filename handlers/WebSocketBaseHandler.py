# -*- coding: utf-8 -*-
# @Author  :songtao

import json
import tornado.web

# from utils.session import Session
from tornado.websocket import WebSocketHandler

class WebSocketBaseHandler(WebSocketHandler):

    @property
    def db(self):
        return self.application.db

    def open(self, *args, **kwargs):
        pass

    def on_close(self):
        pass

    def check_origin(self, origin):
        return True  # 允许WebSocket的跨域请求


class StaticFileHandler(tornado.web.StaticFileHandler):
    def __init__(self, *args, **kwargs):
        super(StaticFileHandler, self).__init__(*args, **kwargs)





