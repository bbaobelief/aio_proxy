import aiohttp
import asyncio

#proxy="http://180.97.193.58:3128"
proxy="http://114.250.25.19:80"

async def get():
  async with aiohttp.ClientSession() as session:
    async with session.get('https://www.baidu.com', timeout=20, proxy=proxy) as resp:
      print(resp.status)
      assert resp.status == 200
      print(await resp.text())
     # html = await resp.text(encoding='utf-8')


loop = asyncio.get_event_loop()
loop.run_until_complete(get())
