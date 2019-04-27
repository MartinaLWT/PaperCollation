#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Basic run script"""

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.autoreload
from tornado.options import options
import tornado.web
import logging
from settings import settings
from paper_assistant.urls import url_patterns


class TornadoApplication(tornado.web.Application):

    def __init__(self):
        tornado.web.Application.__init__(self, url_patterns, **settings)
        self.executor = tornado.concurrent.futures.ThreadPoolExecutor(16)


def main():
    options.parse_command_line()
    app = TornadoApplication()
    app.listen(options.port)
    logging.info("start service at: {}".format(options.port))
    tornado.ioloop.IOLoop.current().start()
    logging.info("stop service")


if __name__ == "__main__":
    main()
