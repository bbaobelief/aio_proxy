# -*- coding: UTF-8 -*-




class Proxy:
    def __init__(self, ip):
        self._url = 'http://' + ip
        self._score = 100

    @property
    def url(self):
        return self._url

