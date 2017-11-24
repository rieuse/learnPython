import redis
from multiprocessing import Process

r = redis.StrictRedis(host='127.0.0.1', port=6379)
print(r.scard("douban_user_id"))

Process.start()
