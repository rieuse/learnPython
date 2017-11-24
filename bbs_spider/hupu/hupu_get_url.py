import json
import random
import time
import multiprocessing
import logging
import pymongo
import re
import redis
import threadpool
from bs4 import BeautifulSoup
import requests
from lxml import etree
import sys
from bloomfilterOnRedis import BloomFilter

sys.setrecursionlimit(1000000)
logger = logging.getLogger('log')
logger.setLevel(logging.INFO)

fh = logging.FileHandler('hupu_log.txt')
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)

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
    'User-Agent': random.choice(UA_LIST),
    'cookie': '_HUPUSSOID=c30a3e85-ebd8-46fc-9334-5465efcf0a9c; _CLT=b0c2a05996d8b48b354e1fa4ddfc1fef; u=32023008|5LiN6IKv5byA5Y+j|1068|568bcea6bff5398192f8e5c114a67672|bff5398192f8e5c1|aHVwdV9kMzQ2ZDdmNzc3M2RlZDIz; ua=167118528; us=c6ca7d7b9ac259050de5dc9b81c685aef48811e617e8f2f726936e63098abd2ec94637f0c28491b573024fe19eb734647dfaa40c15fd904301c84b4c9c0caa68'
}
clients = pymongo.MongoClient('localhost')
db = clients["bbs"]
col = db["hupu_cba_all_url"]

proxies = {
    'http': "http://HW2XS2E6K7BA276D:9688CB7DA500A54D@http-dyn.abuyun.com:9020",
    'https': "http://HW2XS2E6K7BA276D:9688CB7DA500A54D@http-dyn.abuyun.com:9020"
}


def to_bloom(link):
    bf = BloomFilter()
    bf.insert(link)


def to_redis(data):
    r = redis.StrictRedis(host='127.0.0.1', port=6379)
    print("{} into redis".format(data))
    r.sadd("hupu_topic_url", '{}'.format(data))


def pop_redis():
    r = redis.StrictRedis(host='127.0.0.1', port=6379, decode_responses=True)
    po = r.spop("hupu_topic_url")
    return po


def to_redis_error(data):
    r = redis.StrictRedis(host='127.0.0.1', port=6379)
    print("{} into redis".format(data))
    r.sadd("hupu_topic_url_error", '{}'.format(data))


def get_link(url):
    logger.info(url)
    # with open('hupu_url_log.txt','w') as f:
    #     f.write(url)
    html = requests.get(url, headers=headers).content.decode('utf-8')
    hrefs = etree.HTML(html).xpath('//td[@class="p_title"]/a/@href')
    print(hrefs)
    for i in hrefs:
        link = 'https://bbs.hupu.com' + i
        print(link)
        # get_detail(link)


def get_detail(link):
    print(link)
    bf = BloomFilter()
    if not bf.isContains(link):
        dic = {'url': link}
        col.insert(dic)
        bf.insert(link)
        try:
            next_page(link)
        except  Exception as e:
            print(e)
    else:
        logger.warning('exists : {}'.format(link))


def next_page(link):
    html = requests.get(link, headers=headers).content.decode('utf-8')
    next_url = etree.HTML(html).xpath('//*[@id="j_next"]/@href')
    if next_url:
        next_url = 'https://bbs.hupu.com' + next_url[0]
        # logger.info('next_url: {}'.format(next_url))
        get_detail(next_url)


def thread_main(item):
    pool = threadpool.ThreadPool(20)
    tasks = threadpool.makeRequests(get_link, item)
    [pool.putRequest(req) for req in tasks]
    pool.wait()


def multipro_main(item):
    pool = multiprocessing.Pool(1)
    pool.map(get_link, item)
    pool.close()
    pool.join()


def get_start_urls():
    url1 = 'https://bbs.hupu.com/get_nav?fup=174'
    data = requests.get(url1).json()
    album_urls = ['https:' + i['url'] for i in data['data']]
    for album_url in album_urls[:]:
        print(album_url)
        ht = requests.get(album_url).content.decode('utf-8')
        page = re.findall(r'(?<=共).+(?=主题)', ht)
        if page:
            page_num = int(page[0]) / 100
            print(page_num)
            start_urls = ['{}-{}'.format(album_url, n) for n in range(2536, int(page_num))]
            # print(start_urls)
            thread_main(start_urls)
            logger.info('over  : {}'.format(album_url))
            return
            # return start_urls


if __name__ == '__main__':
    get_link('https://bbs.hupu.com/bxj-2536')
    # get_detail('')
    # get_start_urls()
    # multipro_main(start_urls)


# https://bbs.hupu.com/get_nav?fup=232
# https://bbs.hupu.com/get_nav?fup=198  zhuqiu
# https://bbs.hupu.com/get_nav?fup=4596 china
# https://bbs.hupu.com/get_nav?fup=41
# https://bbs.hupu.com/get_nav?fup=174
