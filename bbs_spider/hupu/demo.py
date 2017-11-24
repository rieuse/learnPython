import pymongo
import redis

clients = pymongo.MongoClient('localhost')
db = clients["sougou"]

col = db['info']
col1 = db["hupu_topic_url"]
col2 = db["hupu_topic-1"]


def to_redis(data):
    r = redis.StrictRedis(host='127.0.0.1', port=6379)
    print("{} into redis".format(data))
    r.sadd("hupu_nba1_set", '{}'.format(data))


def pop_redis():
    r = redis.StrictRedis(host='127.0.0.1', port=6379, decode_responses=True)
    po = r.spop("hupu_nba1_set")
    return po


r = redis.StrictRedis(host='127.0.0.1', port=6379, decode_responses=True)
print(r.scard('hupu_nba1_set'))
print(r.scard('zhihu_user_id'))

# for i in col.find():
#     print(type(i),i)
#     col.find_one_and_delete(filter=i)
#     break
