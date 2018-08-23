import time
from rq import Queue
import redis
from rs import count_words_at_url

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
conn = redis.Redis(connection_pool=pool)
q = Queue('ip',connection=conn, timeout=1)

for i in range(100):
  job = q.enqueue(count_words_at_url, 'http://www.baidu.com')

