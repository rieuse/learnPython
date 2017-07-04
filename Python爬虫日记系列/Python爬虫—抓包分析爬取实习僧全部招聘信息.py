import json
import requests
import pymongo
import time

clients = pymongo.MongoClient('localhost')
db = clients["Shixiseng"]
col = db["detail_info"]

urls = ['http://www.shixiseng.com/app/internsvt?c=%E5%85%A8%E5%9B%BD&p={}&t=hot'.format(n) for n in range(1, 3487)]
for url in urls:
    print(url)
    r = requests.get(url)
    html = r.content.decode('utf-8')
    content = json.loads(html)['msg']['b']
    for i in content:
        print('插入一条数据：')
        print(i)
        col.insert(i)
    time.sleep(0.01)
