import asyncio
import concurrent.futures
import requests
import pickle
from memory_profiler import profile

success = []

def req(proxy):
    print(':>', proxy)
    try:
        r = requests.get('http://www.chinaz.com/', timeout=5, proxies={'http': proxy})
        if 'chinaz.com' in r.text:
            return proxy
            #success.append(proxy)
            #print(r.text)
    except Exception as e:
        #print(e)
        pass

async def main():
    pkl_file = open('proxy.pkl', 'rb')
    data = pickle.load(pkl_file)
    print('proxy:', len(data))  
    pkl_file.close()

    with concurrent.futures.ThreadPoolExecutor(max_workers=5000) as executor:
        loop = asyncio.get_event_loop()
        futures = [loop.run_in_executor(executor, req, "http://{host}:{port}".format(host=i['host'], port=i['port'])) for i in data[:50000]]
        for res in await asyncio.gather(*futures):
            if res:
                success.append(res)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

import pprint
print('Total:',len(success))
pprint.pprint(success)
