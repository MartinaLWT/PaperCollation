# -*- coding: utf-8 -*-

"""Global settings for the project"""

import os.path

from tornado.options import define

define("port", default=8000, help="run on the given port", type=int)
define("config", default=None, help="tornado config file")
define("debug", default=False, help="debug mode")

__BASE_PACKAGE__ = "paper_assistant"

settings = {}

settings["debug"] = True
settings["cookie_secret"] = "XBFMXATzBX8tERMddLIJCfrXs"
settings["login_url"] = "/login"
settings["static_path"] = os.path.join(os.path.dirname(__file__), __BASE_PACKAGE__, "static")
settings["template_path"] = os.path.join(os.path.dirname(__file__), __BASE_PACKAGE__, "templates")
settings["xsrf_cookies"] = False

# data = [
#     {
#         "Author": "Buzhou Tang, Hongxin Cao, Xiaolong Wang, Qingcai Chen, Hua Xu",
#         "title": "Evaluating word representation features in biomedical named entity recognition tasks",
#         "published_date": "2014",
#         "Publication": "BioMed research international",
#         "Publication search details": {"message1": 'xx',
#                                        "message2": 'xx'},
#         "other": []
#     },
#     {
#         "Author": "Buzhou Tang, Hongxin Cao, Xiaolong Wang, Qingcai Chen, Hua Xu",
#         "title": "Evaluating word representation features in biomedical named entity recognition tasks",
#         "published_date": "2014",
#         "Publication": "BioMed research international",
#         "Publication search details": {"message1": 'xx',
#                                        "message2": 'xx'},
#         "other": []
#     },
#     {
#         "Author": "Buzhou Tang, Hongxin Cao, Xiaolong Wang, Qingcai Chen, Hua Xu",
#         "title": "Evaluating word representation features in biomedical named entity recognition tasks",
#         "published_date": "2014",
#         "Publication": "BioMed research international",
#         "Publication search details": {"message1": 'xx',
#                                        "message2": 'xx'},
#         "other": []
#     },
# ]
