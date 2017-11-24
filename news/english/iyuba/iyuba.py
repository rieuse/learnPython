import os
import re
import pymongo
import requests
from lxml import etree
from pybloom import BloomFilter
import logzero
from logzero import logger
import time
from fake_useragent import UserAgent
from multiprocessing.dummy import Pool as thpool

ua = UserAgent()
clients = pymongo.MongoClient('localhost')
db = clients["news"]
col1 = db["iyuba"]
col2 = db["iyuba-url"]
logzero.logfile('iyuba.log', maxBytes=500 * 1024 ^ 3)
# filter = BloomFilter(capacity=15*(8*1024*1024), error_rate=0.001) # 1Mb可以去重58 - 80 万数据

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control': 'max-age=0',
    'Proxy-Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Referer': 'http://news.iyuba.com/',
    'User-Agent': ua.random,
}


def get_links():
    url = 'http://news.iyuba.com/'
    html = requests.get(url, headers=headers).content.decode('utf-8')
    links = etree.HTML(html).xpath('//*[@id="page_header"]/div[4]/div/div[2]/ul/li/a/@href')
    return links[1:]


def get_mp3(url):
    html = requests.get(url, headers).content
    if not os.path.exists('source'):
        print('创建文件夹...')
        os.makedirs('source')
    filename = 'source\\{}'.format(url[-9:-4]) + '.mp3'
    with open(filename, 'wb') as f:
        f.write(html)
    logger.info(url)


def parse_link(link):
    html = requests.get(link, headers).content
    detail_url = etree.HTML(html).xpath('//*[@id="content"]/div[1]/div/a/@href')
    if detail_url:
        detail_url = ['http://news.iyuba.com' + i[:-4] + 'mp3' for i in detail_url]
        # print(detail_url)
        thread_pool(detail_url)
    else:
        logger.warn('parse error' + link)
    next_url = next_page(html)
    if next_url:
        parse_link(next_url)
    else:
        logger.info('over')


def next_page(html):
    # html = requests.get(url,headers=headers).content
    next_url = ''.join(etree.HTML(html).xpath('//*[@id="content"]/div[1]/div/div/ul/li[7]/a/@href'))
    if next_url:
        next_url = 'http://news.iyuba.com/' + next_url[6:]
    return next_url


def thread_pool(item):
    pool = thpool(8)
    pool.map(get_mp3, item)
    pool.close()
    pool.join()


if __name__ == '__main__':
    links = get_links()
    for link in links:
        parse_link(link)
