# -*- coding: utf-8 -*-

from paper_assistant.handlers import base, paper_assistant

url_patterns = [
    (r"/", base.MainHandler),
    (r"/api/v0/assistant", paper_assistant.PaperHandler)
]
