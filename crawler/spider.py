# -*- coding: UTF-8 -*-

import re
import requests

headers = {'Upgrade-Insecure-Requests':'1',
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
	#	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	#	'Referer':'http://www.xicidaili.com/nn/',
	#	'Accept-Encoding':'gzip, deflate, sdch',
#		'Accept-Language':'zh-CN,zh;q=0.8',
	  }   



class Spider(object):
    def __init__(self, ip=''):
        self._url = 'http://' + ip
        self._score = 100

    def get(self):
        url = "http://m.66ip.cn/{}.html" 
        print(url.format(1))
        S = requests.Session()
        r = S.get(url, headers=headers)

        print(r.headers)
        print(r.status_code)
        #html = requests.get(url, headers=headers).content
        #html = html.decode(chardet.detect(html)['encoding'])
        #pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}'
        #all_ip = re.findall(pattern, html)
        #print(all_ip)


s = Spider()
print(s.get())
