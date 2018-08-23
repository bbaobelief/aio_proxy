import redis
from rq import Worker, Queue, Connection

listen = ['high', 'default', 'low', 'ip']

pool = redis.ConnectionPool(db=0, host='localhost', port=6379)
conn = redis.Redis(connection_pool=pool)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()
