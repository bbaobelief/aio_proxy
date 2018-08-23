# -*- coding: UTF-8 -*-

import re
import time
import asyncio
import aiohttp
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from concurrent import futures
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
loop = asyncio.get_event_loop()

class Spider(object):

    def __init__(self, loop, maxtasks=5, timeout=10*1, page=20):
        self.result = [] 
        self.page = page
        self.loop = loop
        self.sem = asyncio.Semaphore(maxtasks, loop=loop)
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.connector = aiohttp.TCPConnector(verify_ssl=False, use_dns_cache=True)
        self.proxy= "{type}://{host}:{port}"
       # self.session = aiohttp.ClientSession(loop=loop, timeout=self.timeout)

        self.urls = ['https://www.kuaidaili.com/free/inha/{page}/', 'https://www.kuaidaili.com/free/intr/{page}/'] 
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36"
        }
       
        self.cookies = {'Cookie': '_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJTk3YjkwNDMzYzg2Nzc0N2Q2YWUwMjk4OTNjZDViNDk3BjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMTBBdVJqSXlEZ29EYjI0cS82TTJzZm5kcldRYTd4QzlqTlJkRDlwdC9DZmc9BjsARg%3D%3D--04b43d268d7535bdeab77c97858adfda9e7fc0e8; Hm_lvt_0cf76c77469e965d2957f0553e6ecf59=1530003408,1530776861,1530778901,1530779353; Hm_lpvt_0cf76c77469e965d2957f0553e6ecf59=1531210299'}
       
    async def fetch_page(self, url):
        print('running: {0}'.format(url))
        async with self.sem:
            async with aiohttp.ClientSession(loop=self.loop, timeout=self.timeout) as session:
                async with session.get(url, headers=self.headers) as res:
                    try:
                        assert res.status == 200
                        print("Success: {0}, {1}".format(res.status, res.url))
                        html = await res.text()
                        return res.status, html
                    except AssertionError:
                        print('Fail: {0}, {1}'.format(res.status, res.url))
                        return res.status, None 

    async def parse_page(self, url):
        status, page = await self.fetch_page(url)
        if page:
            soup = BeautifulSoup(page, 'lxml')
            for tr in soup.findAll('tr'):
                tds = tr.findAll('td')
                if tds:
                   info = {
                       "host": tds[1].get_text().strip(),
                       "port": tds[2].get_text().strip(),
                       "anonymity": tds[4].get_text().strip(),
                       "type": tds[5].get_text().strip().lower(),
                       "region": tds[3].get_text().strip(),
                       "rtime": tds[7].div.get('title').strip(),
                       "from": url.split('/')[2],
                   }
                   self.result.append(info)
        import pprint
        #pprint.pprint(self.result)
        print('\n Total: %s' % len(self.result))
        return self.result

    async def verify_proxy(self, proxy):
        print('Proxy:', proxy)
        try:
            async with aiohttp.ClientSession(loop=loop) as session:
                start = time.time()
                async with session.get("https://www.baidu.com", proxy=proxy, timeout=2) as resp:
                    end = time.time()
                    print(resp.status)
                    assert resp.status == 200
                    print('Good proxy: {} {}s'.format(proxy, end-start))
                    return True
        except asyncio.TimeoutError as e:
            # print('Timeout: {}'.format(e))
            pass
        except aiohttp.client_exceptions.ServerDisconnectedError as e:
            # print('ServerDisconnectedError')
            pass
        except aiohttp.client_exceptions.ClientProxyConnectionError as e:
            # print('ClientProxyConnectionError')
            pass
        except aiohttp.client_exceptions.ClientHttpProxyError as e:
            # print('ClientHttpProxyError')
            pass


    async def close(self):
        self.session.close()

    async def run(self):
        pass



def main():
    s = Spider(loop=loop)
    url = 'http://www.xicidaili.com/nt/{page}/'
    tasks = [asyncio.ensure_future(s.parse_page(url.format(page=i)), loop=loop) for i in range(1, 101)]
    futures = asyncio.gather(*tasks)
    result = loop.run_until_complete(futures)
    import pprint
    import pickle
    #pprint.pprint(result)    
    res = []
    for i in result:
        res.extend(i)
        print(i)
   
    with open('ip.pkl', 'wb+') as f:
        pickle.dump(res, f)
   
    loop.close()


if __name__ == '__main__':
    main()         

