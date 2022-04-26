# -*- coding: utf-8 -*-
"""
@File: tornado_framework.py 
@Time : 2022/4/26 19:36
@dec: 
"""


import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.gen
import tornado.autoreload
from tornado.concurrent import run_on_executor
from tornado.options import define, options
from concurrent.futures import ThreadPoolExecutor

import json
import traceback

port = ...  # 端口
luyou = ...  # 路由

define("port", default=port, help="run on the given port", type=int)


class IndexHandler(tornado.web.RequestHandler):
    def __init__(self, *args, **kwargs):
        super(IndexHandler, self).__init__(*args, **kwargs)
        try:
            self.executor = ThreadPoolExecutor(1000)
            ...  # 初始化操作
        except Exception as e:
            raise e

    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        # 获取入参主体
        post_data = self.request.body_arguments
        post_data = {x: post_data.get(x)[0].decode("utf-8") for x in post_data.keys()}
        if not post_data:
            post_data = self.request.body.decode("utf-8")
            post_data = json.loads(post_data)

        res = self.handleBlock(**post_data)
        res = yield res
        self.write(res)
        self.finish()

    @tornado.gen.coroutine
    def put(self, *args, **kwargs):
        # 对入参进行解析
        get_data = self.request.body_arguments
        get_data = {x: get_data.get(x)[0].decode("utf-8") for x in get_data.keys()}
        if not get_data:
            get_data = self.request.body.decode("utf-8")
            get_data = json.loads(get_data)

        res = yield self.updateBlock(**get_data)
        self.write(res)
        self.finish()

    @run_on_executor
    def handleBlock(self, *args, **kwargs):
        try:
            return self._handle(*args, **kwargs)
        except Exception as e:
            return {"code": -1, "error": "operate success with {}.{}".format(e, traceback.format_exc())}

    def _handle(self, *args, **kwargs):
        """
        post的核心编码模块
        """
        return {"code": 1, "message": "operate success"}

    @run_on_executor
    def updateBlock(self, *args, **kwargs):
        try:
            return self._update(*args, **kwargs)
        except Exception as e:
            return {"code": -1, "error": "update failed with {}.{}".format(e, traceback.format_exc())}

    def _update(self, *args, **kwargs):
        """
        update的核心编码模块
        """
        return {"code": 1, "message": "update success"}


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(luyou, IndexHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
