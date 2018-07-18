import pprint, pickle
import asyncio
import aiohttp
from aiohttp.client_exceptions import ClientProxyConnectionError
from aiohttp.client_exceptions import ClientHttpProxyError
from aiohttp.client_exceptions import ClientConnectorError
from aiohttp.client_exceptions import ServerDisconnectedError
from concurrent.futures._base import TimeoutError
result = []
semaphore = asyncio.Semaphore(50)
from memory_profiler import profile

@profile
async def verify_proxy(proxy):
  #print('>:', proxy)
  #print('start work')
  await asyncio.sleep(5)
  #with await semaphore:
  #    async with aiohttp.ClientSession() as session:
  #      try:
  #        async with session.get('https://www.baidu.com', timeout=3, proxy=proxy) as resp:
  #          #assert resp.status == 200
  #          print(await resp.text())
  #          if 'baidu.com' in await resp.text():
  #              print(proxy)
  #              #result.append(proxy)
  #      except Exception as e:
  #          pass
  #print('end work')

@profile
async def main():
    success = []
    pkl_file = open('proxy.pkl', 'rb')
    data = pickle.load(pkl_file)
    print('proxy:', len(data))  
    pkl_file.close()

    proxy = "http://{host}:{port}" 
    tasks = [asyncio.ensure_future(verify_proxy(proxy.format(host=i['host'], port=i['port']))) for i in data[:10000]]
    await asyncio.gather(*tasks)
 
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main()) 

    print('result', len(result)) 
    pprint.pprint(result)

