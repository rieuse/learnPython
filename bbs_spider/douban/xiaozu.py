import json
import pymongo
import redis
import requests
import time
from lxml import etree
import sys
from pybloom import BloomFilter
import logzero
from bs4 import BeautifulSoup
from logzero import logger
from fake_useragent import UserAgent
from multiprocessing.dummy import Pool as thpool

ua = UserAgent()
sys.setrecursionlimit(1000000)
clients = pymongo.MongoClient('localhost')
startcol = ''
db = clients["bbs"]
col1 = db["douban"]
col2 = db["douban-last"]
logzero.logfile('douban.log', maxBytes=50 * 1024 ^ 3)
filter = BloomFilter(capacity=15 * (8 * 1024 * 1024), error_rate=0.001)  # 1Mb可以去重58 - 80 万数据

proxies = {
    'http': "http://HI754098W055I8BD:C3537F5006B483C5@http-dyn.abuyun.com:9020",
    'https': "http://HI754098W055I8BD:C3537F5006B483C5@http-dyn.abuyun.com:9020"
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control': 'max-age=0',
    'Proxy-Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Referer': 'https://www.douban.com/group/explore',
    'User-Agent': ua.random,
}


def to_redis(data):
    r = redis.StrictRedis(host='127.0.0.1', port=6379)
    # print("{} into redis".format(data))
    r.sadd("douban_user_id", '{}'.format(data))


def pop_redis():
    r = redis.StrictRedis(host='127.0.0.1', port=6379, decode_responses=True)
    po = r.spop("douban_user_id")
    return po


def judge_redis(str):
    r = redis.StrictRedis(host='127.0.0.1', port=6379)
    ss = r.sismember("douban_user_id", str)
    return ss


def Generator(follows):
    for i in follows:
        yield i


def get_follow(url):
    # url = 'https://www.douban.com/people/{}/'.format(id)
    html = requests.get(url, headers=headers).text
    follows = etree.HTML(html).xpath('//*[@id="friend"]/dl/dd/a/@href')
    logger.info(follows)
    for i in follows:
        to_redis(i)
    mygenerator = Generator(follows)
    for i in mygenerator:
        get_follow(i)


if __name__ == '__main__':
    start_url = 'https://www.douban.com/people/nw77/'
    get_follow(start_url)
