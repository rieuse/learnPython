import json
import random
import time
import multiprocessing
import logging
from math import ceil

import pymongo
import re
import redis
import threadpool
from bs4 import BeautifulSoup
import requests
from lxml import etree
import sys
# from bloomfilter_Redis import BloomFilter
from pybloom import BloomFilter

sys.setrecursionlimit(1000000)
logger = logging.getLogger('log')
logger.setLevel(logging.INFO)

fh = logging.FileHandler('hupu_log_zijian.txt')
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
    'cookie': '_dacevid3=101fc2c5.de03.9451.383c.b105be3358ec; _HUPUSSOID=8ab2d9aa-1a7a-4287-9a7c-b684483cecce; _CLT=b0c2a05996d8b48b354e1fa4ddfc1fef; u=32023008|5LiN6IKv5byA5Y+j|1068|568bcea6bff5398192f8e5c114a67672|bff5398192f8e5c1|aHVwdV9kMzQ2ZDdmNzc3M2RlZDIz; ua=167197648; us=74fb49fcefe48a7be92fcbd39288e3e3f48811e617e8f2f726936e63098abd2ec94637f0c28491b573024fe19eb734648a31e366994c73f62094a41cbe110e75; __dacevst=44f2fefb.4e9001ca|1504780711902; _cnzz_CV30020080=buzi_cookie%7C101fc2c5.de03.9451.383c.b105be3358ec%7C-1; Hm_lvt_39fc58a7ab8a311f2f6ca4dc1222a96e=1504151532,1504176436,1504238400,1504778913; Hm_lpvt_39fc58a7ab8a311f2f6ca4dc1222a96e=1504778913; Hm_lvt_6cda846867fd596b2ca7a177bac2039f=1504778776; Hm_lpvt_6cda846867fd596b2ca7a177bac2039f=1504778913'
}
clients = pymongo.MongoClient('localhost')
db = clients["bbs"]
col = db["hupu_cba_all_url"]

proxies = {
    'http': "http://HW2XS2E6K7BA276D:9688CB7DA500A54D@http-dyn.abuyun.com:9020",
    'https': "http://HW2XS2E6K7BA276D:9688CB7DA500A54D@http-dyn.abuyun.com:9020"
}

filter = BloomFilter(capacity=20 * (8 * 1024 * 1024), error_rate=0.001)  # 1Mb可以去重58 - 80 万数据


def add_bloom_from_mongo():
    print('add user_id to bloomfilter form mongodb')
    for i in col.find():
        filter.add(i['url'])
    print('over')


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
    # with open('hupu_url_log.txt','w') as f:
    #     f.write(url)
    html = requests.get(url, headers=headers).content.decode('utf-8')
    hrefs = etree.HTML(html).xpath('//td[@class="p_title"]/a/@href')
    if not hrefs:
        hrefs = etree.HTML(html).xpath('//div[@class="titlelink box"]/a/@href')
    logger.info('{}   {}'.format(url, len(hrefs)))
    for i in hrefs:
        link = 'https://bbs.hupu.com' + i
        print(link)
        get_detail(link)


def get_detail(link):
    print(link)
    if not link in filter:
        dic = {'url': link}
        col.insert(dic)
        filter.add(link)
        try:
            next_page(link)
        except  Exception as e:
            logger.warning(e)
    else:
        pass
        # logger.warning('exists : {}'.format(link))


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
    url1 = 'https://bbs.hupu.com/get_nav?fup=114'
    data = requests.get(url1, headers=headers).json()
    album_urls = ['https:' + i['url'] for i in data['data']]
    for album_url in album_urls[:]:
        print(album_url)
        ht = requests.get(album_url).content.decode('utf-8')
        page = re.findall(r'(?<=共).+(?=主题)', ht)
        if page:
            page_num_min = ceil(int(page[0]) / 100)
            page_num = ceil(int(page[0]) / 40)
            print(page_num)
            start_urls = ['{}-{}'.format(album_url, n) for n in range(page_num_min, int(page_num))]
            # print(start_urls)
            thread_main(start_urls)
            logger.info('over  {}'.format(album_url))
            # return
            # return start_urls


if __name__ == '__main__':
    add_bloom_from_mongo()
    # get_link('https://bbs.hupu.com/bxj-2549')
    # get_detail('https://bbs.hupu.com/2988548.html')
    get_start_urls()
    # multipro_main(start_urls)

# 步行街 12开始40

# https://bbs.hupu.com/get_nav?fup=232
# https://bbs.hupu.com/get_nav?fup=198  zhuqiu
# https://bbs.hupu.com/get_nav?fup=4596 china 
# https://bbs.hupu.com/get_nav?fup=41
# https://bbs.hupu.com/get_nav?fup=174   bxj end with  2536
# https://bbs.hupu.com/lol-647
