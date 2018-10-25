# -*- coding: utf-8 -*-
# @Author  :songtao

import json
import tornado.web

# from utils.session import Session
from tornado.web import RequestHandler, StaticFileHandler

class BaseHandler(RequestHandler):

    @property
    def db(self):
        return self.application.db

    def prepare(self):
        self.xsrf_token
        if self.request.headers.get("Content-Type", "").startswith("application/json"):
            self.json_args = json.loads(self.request.body.decode('utf-8'))
        else:
            self.json_args = None

    def write_error(self, status_code, **kwargs):
        pass

    def set_default_headers(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")

    def initialize(self):
        pass

    def on_finish(self):
        pass


class StaticFileHandler(tornado.web.StaticFileHandler):
    def __init__(self, *args, **kwargs):
        super(StaticFileHandler, self).__init__(*args, **kwargs)





