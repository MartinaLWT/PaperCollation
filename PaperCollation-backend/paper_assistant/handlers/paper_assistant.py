from paper_assistant.handlers import base
from paper_assistant.model import paper_data

from flask import Flask, jsonify, render_template, request, flash
from flask import redirect,url_for

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

