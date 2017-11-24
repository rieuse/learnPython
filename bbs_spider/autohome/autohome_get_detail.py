import json
import random
import threading
import time
import multiprocessing
import pymongo
import redis
import threadpool
from bs4 import BeautifulSoup
import requests
from lxml import etree
import sys

sys.setrecursionlimit(1000000)
clients = pymongo.MongoClient('localhost')
db = clients["bbs"]
col = db["autohome-1"]

UA_LIST = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control': 'max-age=0',
    'Proxy-Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': random.choice(UA_LIST)
}

proxies = {
    'http': "http://HW2XS2E6K7BA276D:9688CB7DA500A54D@http-dyn.abuyun.com:9020",
    'https': "http://HW2XS2E6K7BA276D:9688CB7DA500A54D@http-dyn.abuyun.com:9020"
}


def to_redis(data):
    r = redis.StrictRedis(host='127.0.0.1', port=6379)
    print("{} into redis".format(data))
    r.sadd("autohome1_set", '{}'.format(data))


def pop_redis():
    r = redis.StrictRedis(host='127.0.0.1', port=6379, decode_responses=True)
    po = r.spop("autohome1_set")
    return po


def to_redis_error(data):
    r = redis.StrictRedis(host='127.0.0.1', port=6379)
    print("{} into redis".format(data))
    r.sadd("autohome1_error", '{}'.format(data))


def detail():
    while True:
        url = pop_redis()
        try:
            html = requests.get(url, headers=headers, proxies=proxies).content.decode('GBK')
            title = ''.join(etree.HTML(html).xpath('//*[@id="F0"]/div[2]/div[2]/h1/div/text()'))
            content = ''.join(etree.HTML(html).xpath('//*[@id="F0"]/div[2]/div[2]/div[1]/div/div[2]/text()'))
            # comment = etree.HTML(html).xpath('//*[@id="maxwrap-reply"]div/div[2]/div[1]/div[2]/div/text()')
            # comment = etree.HTML(html).xpath('//div[@class="w740"]/text()')
            comment = BeautifulSoup(html, 'html.parser').find_all('div', class_="w740")
            # print(comment)
            comments = []
            for i in comment:
                comments.append(i.get_text())
            comments = sorted(set(comments), key=comments.index)
            dic = {
                'title': title,
                'content': content,
                'comments': comments
            }
            print(title)
            col.insert(dic)
        except Exception as e:
            print(e)
            to_redis(url)
            html = requests.get(url, headers=headers, proxies=proxies).content.decode('GBK')
            title = ''.join(etree.HTML(html).xpath('//*[@id="F0"]/div[2]/div[2]/h1/div/text()'))
            content = ''.join(etree.HTML(html).xpath('//*[@id="F0"]/div[2]/div[2]/div[1]/div/div[2]/text()'))
            # comment = etree.HTML(html).xpath('//*[@id="maxwrap-reply"]div/div[2]/div[1]/div[2]/div/text()')
            # comment = etree.HTML(html).xpath('//div[@class="w740"]/text()')
            comment = BeautifulSoup(html, 'html.parser').find_all('div', class_="w740")
            # print(comment)
            comments = []
            for i in comment:
                comments.append(i.get_text())
            comments = sorted(set(comments), key=comments.index)
            dic = {
                'title': title,
                'content': content,
                'comments': comments
            }
            print(title)
            col.insert(dic)


if __name__ == '__main__':
    task = []
    for _ in range(1, 15):
        task.append(threading.Thread(target=detail))
    for t in task:
        t.start()
    for t in task:
        t.join()
