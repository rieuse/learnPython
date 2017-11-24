import threading
import pymongo
import redis
import requests
from concurrent import futures
from lxml import etree
import sys
from pybloom import BloomFilter
import logzero
from logzero import logger
from fake_useragent import UserAgent

ua = UserAgent()
sys.setrecursionlimit(1000000)
clients = pymongo.MongoClient('localhost')
lock = threading.Lock()
db = clients["bbs"]
col1 = db["douban"]
col2 = db["douban-group-content"]
logzero.logfile('douban-content.log', maxBytes=50 * 1024 ^ 3)
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


def pop_redis():
    r = redis.StrictRedis(host='127.0.0.1', port=6379, decode_responses=True)
    po = r.spop("douban_user_id")
    return po


def Generator(follows):
    for i in follows:
        yield i


def parser(url):
    html = requests.get(url, headers=headers).text
    title = etree.HTML(html).xpath('//*[@id="content"]/h1/text()')
    if title:
        title = title[0].strip()
    else:
        return
    content = ''.join(etree.HTML(html).xpath('//*[@id="link-report"]/div/p/text()'))
    comment = etree.HTML(html).xpath('//*[@id="comments"]/li/div[2]/p/text()')
    doc = {
        'url': url,
        'title': title,
        'content': content,
        'comment': comment
    }
    with lock:
        col2.insert(doc)
        print(doc)


def get_links(url):
    html = requests.get(url, headers=headers).text
    links = etree.HTML(html).xpath('//td[@class="title"]/a/@href')
    print(links)
    with futures.ThreadPoolExecutor(10) as executor:
        executor.map(parser, links)


def main(url):
    frist_url = '{}discussion?start=0'.format(url)
    html = requests.get(frist_url, headers=headers).text
    nums = ''.join(etree.HTML(html).xpath('//*[@id="content"]/div/div[1]/div[3]/a[last()]/text()'))
    if nums:
        nums = int(nums) - 1
    else:
        print('get page nums error')
    print(nums)
    urls = ['{}discussion?start={}'.format(url, num) for num in range(0, nums, 25)]
    gen = Generator(urls)
    for i in gen:
        logger.info(i)
        get_links(i)


if __name__ == '__main__':
    # while True:
    #     start_url = pop_redis()
    #     main(start_url)
    start_url = 'https://www.douban.com/group/148218/'
    main(start_url)
