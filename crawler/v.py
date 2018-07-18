

class Proxy:
    def __init__(self, ip):
        self._url = 'http://' + ip
        self._score = 100

    @property
    def url(self):
        return self._url

    @property
    def score(self):
        return self._score

    def __lt__(self, other):
        '''
        由于优先队列是返回最小的，而这里分数高的代理优秀
        所以比较时反过来
        '''
        return self._score > other._score

    def success(self, time):
        self._score += int(10 / int(time + 1))

    def timeoutError(self):
        self._score -= 10

    def connectError(self):
        self._score -= 30

    def otherError(self):
        self._score -= 50


import pprint, pickle
import requests
from requests.exceptions import ReadTimeout, ProxyError, ConnectTimeout, ChunkedEncodingError

success = []

pkl_file = open('proxy.pkl', 'rb')

data = pickle.load(pkl_file)
for i in data:
  proxies = {"http": "http://{host}:{port}".format(host=i['host'], port=i['port'])}
  #proxies = {"http": "http://35.200.53.16:80"}
  print(proxies)
  try:
      r = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=1, verify=False)
      if r.status_code == 200:
          print(r.status_code)
          print('++++++++++++++++')
          print(r.json())
          success.append(r.json)
          print('----------------')
  except ProxyError as e:
      # print('ProxyError:')
      pass
  except ReadTimeout as e:
      # print('ReadTimeout:')
      pass
  except ConnectTimeout as e:
      # print('ConnectTimeout:')
      pass
  except ChunkedEncodingError as e:
      pass

print(success)
pkl_file.close()
