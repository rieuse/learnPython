import pymongo
import requests
from lxml import etree
import sys
from pybloom import BloomFilter
import logzero
from logzero import logger

from fake_useragent import UserAgent
from multiprocessing.dummy import Pool as thpool

ua = UserAgent()
sys.setrecursionlimit(1000000)
clients = pymongo.MongoClient('localhost')
db = clients["bbs"]
col1 = db["slidot-bbs"]
col2 = db["slidot-url"]
logzero.logfile('slidot.log', maxBytes=50 * 1024 ^ 3)
filter = BloomFilter(capacity=15 * (8 * 1024 * 1024), error_rate=0.001)  # 1Mb可以去重58 - 80 万数据

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control': 'max-age=0',
    'Proxy-Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': ua.random,
}

proxies = {
    'http': "http://H25P63881QWD60HD:4312068F64019001@http-dyn.abuyun.com:9020",
    'https': "http://H25P63881QWD60HD:4312068F64019001@http-dyn.abuyun.com:9020"
}


def add_bloom_from_mongo():
    print('add user_id to bloomfilter form mongodb')
    for i in col2.find():
        filter.add(i['url'])
    print('over')


def get_txt(url):
    logger.info(url)
    if url in filter:
        return
    html = requests.get(url, headers=headers, timeout=6).content
    title = etree.HTML(html).xpath('//*[@id="center"]/div/div[1]/div[1]/div[2]/h2/text()')
    if title:
        title = title[0]
    else:
        return
    content = etree.HTML(html).xpath('//*[@id="center"]/div/div[1]/div[3]/text()')
    ss = [i.strip() for i in content]
    content = ''.join(ss)
    doc = {
        'title': title,
        'content': content
    }
    print(doc)
    col2.insert({'url': url})
    filter.add(url)
    # col1.insert(doc)


def thread_pool(item):
    pool = thpool(20)
    pool.map(get_txt, item)
    pool.close()
    pool.join()


if __name__ == '__main__':
    add_bloom_from_mongo()
    urls = ['http://www.solidot.org/story?sid={}'.format(num) for num in range(1, 53994)]
    thread_pool(urls)
    # for i in urls:
    #     get_txt(i)
    #     exit()
