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
col2 = db["douban-ids"]
logzero.logfile('douban.log', maxBytes=50 * 1024 ^ 3)
filter = BloomFilter(capacity=15 * (8 * 1024 * 1024), error_rate=0.001)  # 1Mb可以去重58 - 80 万数据


def get_proxy():
    url = 'http://ip.16yun.cn:817/myip/tl/beaf0f87-7598-4ccd-a769-5ad34bbaa85c/?s=rvczzrkjka&u=escainew024'
    proxy = requests.get(url).text
    return proxy


proxies = {
    'http': get_proxy(),
    'https': get_proxy()
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


def get_group(url):
    html = requests.get(url, headers=headers).text
    print(html)
    groups = etree.HTML(html).xpath('//*[@id="content"]/div/div[1]/div[2]/div/ul/li[1]/div[2]/div/a/@href')
    print(groups)


if __name__ == '__main__':
    start_url = 'https://www.douban.com/group/people/nw77/joins'
    get_group(start_url)
