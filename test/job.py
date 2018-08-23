import time
from rq import Queue
from redis import Redis
from rs import count_words_at_url

# Tell RQ what Redis connection to use
redis_conn = Redis()
q = Queue('default',connection=redis_conn, timeout=1)  # no args implies the default queue

# Delay execution of count_words_at_url('http://nvie.com')
for i in range(50):
  job = q.enqueue(count_words_at_url, 'http://www.baidu.com')
  print(job.result)   # => None

# Now, wait a while, until the worker is finished
time.sleep(2)
print(job.result)   # => 889
