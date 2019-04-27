from paper_assistant.handlers import base
from paper_assistant.model import paper_data
# 添加GI处理模块
import cgi, cgitb


# 创建FieldStorage的实例化
form = cgi.FieldStorage()
# 获取html页面传递过来的数据值
str_data_1 = form.getvalue('data_1')
str_data_2 = form.getvalue('data_2')
class PaperHandler(base.BaseHandler):
    def get(self):
        search_context = self.get_argument('search_context', None)

        # spider here

        # data = paper_data.data
        # get data from spider
        data = []
        data.append("爬取"+search_context+"得到的内容为：")
        data.append(paper_data.data)
        self.write_success_json(data)


# !/usr/bin/python
# -*- coding: UTF-8 -*-


