# -*- coding: UTF-8 -*-

import re
import requests

class Spider(object):
    def __init__(self, ip):
        self._url = 'http://' + ip
        self._score = 100

    def get(self):
        url = ("http://m.66ip.cn/mo.php?tqsl={proxy_number}")
        url = url.format(proxy_number=10000)
        html = requests.get(url, headers=headers).content
        html = html.decode(chardet.detect(html)['encoding'])
        pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}'
        all_ip = re.findall(pattern, html)


