# -*- coding: utf-8 -*-
import json
import tornado.web


class MainHandler(tornado.web.RequestHandler):
    # @tornado.web.authenticated
    def get(self):
        self.render('demo.html')


class BaseHandler(tornado.web.RequestHandler):
    # @tornado.web.authenticated
    def get(self):
        self.render('index.html')

    def parse_json(self, raw_data):
        if isinstance(raw_data, bytes):
            data = str(raw_data, encoding='utf-8')
        else:
            data = raw_data
        data = json.loads(data)
        return data

    def parse_json_body(self):
        try:
            self.request_data = self.parse_json(self.request.body)
        except (KeyError, ValueError) as e:
            self.write_error(500, "bad json format: {}".format(str(e)))
            self.request_data = None
        return self.request_data

    def parse_query_arguments(self):
        ret = {}
        for k, v in self.request.query_arguments.items():
            if isinstance(v, list) and len(v) != 0:
                if isinstance(v[0], bytes):
                    ret[k] = str(v[0], encoding='utf-8')
                else:
                    ret[k] = v[0]
            else:
                ret[k] = v
        return ret

    def finish_request(self, body):
        self.write(json.dumps(body, sort_keys=True, separators=(',', ': ')))
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.finish()

    def write_success_json(self, data=None):
        self.set_status(200)
        if data is None:
            return self.finish_request({"desc": "success"})
        else:
            return self.finish_request({"desc": "success", "data": data})

    def write_error(self, status_code, desc, reason=None):
        result = {}
        if reason:
            self.set_status(status_code, reason=reason)
        else:
            self.set_status(status_code)
        result['desc'] = desc
        self.finish_request(result)

