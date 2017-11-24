import redis
import pymongo

client = pymongo.MongoClient('localhost')
db = client['bbs']
col = db['hupu_topic_url']

r = redis.StrictRedis(host='127.0.0.1', port=6379)

for i in col.find():
    print(i['url'])
    r.sadd('hupu_topic_1', i['url'])
