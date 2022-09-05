import datetime
import base64
import hashlib
import json

import requests
from django.conf import settings


class YunTongXin():
    Rest_URL = 'https://app.cloopen.com:8883'

    def __init__(self, accountSid, appId, accountToken, templates):
        self.accountSid = accountSid
        self.appId = appId
        self.accountToken = accountToken
        self.templates = templates

    def get_request_url(self, timenow):
        sig = self.accountSid + self.accountToken + timenow

        m = hashlib.md5()
        m.update(sig.encode())
        url = self.Rest_URL + '/2013-12-26/Accounts/%s/SMS/TemplateSMS?sig=%s'%(self.accountSid, m.hexdigest().upper())
        return url

    #请求包头
    def get_header(self, timenow):
        s = self.accountSid+':'+timenow
        authorization = base64.b64encode(s.encode()).decode()
        header = {
            'Accept':'application/json',
            'Content-Type':'application/json;charset=utf-8',
            'Authorization': authorization
        }
        return header

    #请求体
    def get_request_body(self, code, phonenum):
        return {
            'to': phonenum,
            'appId': self.appId,
            'templateId': self.templates,
            'datas': [code, "3"]
        }

    def request_api(self, url, header, body):
        res = requests.post(url=url, headers=header, data=body)
        return res.text

    # 獲取時間
    def get_time(self):
        return datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    def run(self, code, phonenum):
        timenow = self.get_time()
        header = self.get_header(timenow)
        url = self.get_request_url(timenow)
        body = self.get_request_body(code, phonenum)
        data = self.request_api(url, header, json.dumps(body))
        return data




