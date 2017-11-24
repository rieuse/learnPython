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
from pybloom import BloomFilter
import logging

sys.setrecursionlimit(1000000)
clients = pymongo.MongoClient('localhost')
db = clients["bbs"]
col1 = db["tianya-bbs"]
col2 = db["tianya-url"]
filter = BloomFilter(capacity=10 * (8 * 1024 * 1024), error_rate=0.001)  # 1Mb可以去重58 - 80 万数据


def add_bloom_from_mongo():
    print('add user_id to bloomfilter form mongodb')
    for i in col2.find():
        filter.add(i['url'])
    print('over')


# config for logging
logger = logging.getLogger('log')
logger.setLevel(logging.INFO)

fh = logging.FileHandler('tianya_new_log.txt')
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)
# logging.basicConfig(filename='tinaya_shishang_log.txt', format='%(asctime)s %(levelname)s：%(message)s',level=logging.INFO)
UA_LIST = [
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
    # 'cookie': '_dacevid3=748ac4b3.2240.97e1.ca5d.3023e34efe24; _HUPUSSOID=5c904bc3-02a3-4c73-a630-1298ca6a354f; _CLT=b0c2a05996d8b48b354e1fa4ddfc1fef; u=32023008|5LiN6IKv5byA5Y+j|1068|568bcea6bff5398192f8e5c114a67672|bff5398192f8e5c1|aHVwdV9kMzQ2ZDdmNzc3M2RlZDIz; us=4a7ac4a0344d0f42cd093dbb393654f10e187dce817b6bc5b5f349c6de812ddc452edda81a76fd190ac22c90b1c10887af210b8718fe8b6ec2fc28ce3522bf02; _fmdata=4543AD30FB53502925A1CC1A227A8192C6419010310B679335F7B9CBF7FFC05EFDB446EED3ECF143E115FADEE69D04723488662B07B36DEC; ua=166995178; lastvisit=6699%091502956882%09%2Fthread.php%3Fboardname%3Dtopic%26page%3D2; __dacevst=390ffac6.37cb7c32|1502958681045; _cnzz_CV30020080=buzi_cookie%7C748ac4b3.2240.97e1.ca5d.3023e34efe24%7C-1; Hm_lvt_39fc58a7ab8a311f2f6ca4dc1222a96e=1502681042,1502681117,1502760900,1502956607; Hm_lpvt_39fc58a7ab8a311f2f6ca4dc1222a96e=1502956882'
}

proxies = {
    'http': "http://HW2XS2E6K7BA276D:9688CB7DA500A54D@http-dyn.abuyun.com:9020",
    'https': "http://HW2XS2E6K7BA276D:9688CB7DA500A54D@http-dyn.abuyun.com:9020"
}


def get_url_list(url):
    try:
        html = requests.get(url, headers=headers, timeout=4).content
        ls = etree.HTML(html).xpath('//*[@id="bbs_left_nav"]/div[6]/ul/li/a/@href')  # 地区
        ls = ['http://bbs.tianya.cn' + i for i in ls]
        # print(ls, len(ls))
        return ls[17:]
    except:
        get_url_list(url)


ss_url = 'http://bbs.tianya.cn/list-411-1.shtml'
ls = get_url_list(ss_url)


def get_list(url, ls):
    # start_url = 'http://bbs.tianya.cn/list-411-1.shtml'
    print('this list url is :   ', url)
    if url == 'http://bbs.tianya.cnjavascript:history.go(-1)':
        print('over...')
        print(start_url)
        new_url = ls.pop(0)
        if start_url != new_url:
            get_list(new_url, ls)
        return
    if url not in filter:
        # with open('tianya_ask_url_log.txt', 'w') as f:
        #     f.write(url)
        logger.info('URL:  ' + url)
        try:
            html = requests.get(url, headers=headers, timeout=4).content
        except requests.exceptions.ConnectionError:
            html = ''
            get_list(url, ls)
        # print(html.decode('utf-8'))
        lss = etree.HTML(html).xpath(''
                                     '//*[@id="main"]/div[6]/table/tbody/tr/td[1]/a/@href')
        if not lss:
            lss = etree.HTML(html).xpath('//*[@id="main"]/div[7]/table/tbody/tr/td[1]/a/@href')
        detail_list = []
        for i in lss:
            link = 'http://bbs.tianya.cn' + i
            detail_list.append(link)
        thread_main(detail_list)
        # multipro_main(detail_list)
        dic2 = {'url': url}
        col2.insert(dic2)
        filter.add(url)
        next_page(url)
    else:
        logger.warning('exists: {}'.format(url))
        next_page(url)


def next_page(url):
    html = requests.get(url, headers=headers).content
    next_page = etree.HTML(html).xpath('//*[@id="main"]/div[7]/div/a[last()]/@href')
    if not next_page:
        next_page = etree.HTML(html).xpath('//*[@id="main"]/div[8]/div/a[last()]/@href')
    if next_page:
        next_link = 'http://bbs.tianya.cn' + next_page[0]
        if not 'http://bbs.tianya.cn' in next_link:
            next_link = 'http://bbs.tianya.cn' + next_page
        try:
            get_list(next_link, ls)
        except requests.exceptions.Timeout:
            print('error')
            print(next_link)
            # print(next_link)
            get_list(next_link, ls)


def get_detail(url):
    try:
        html = requests.get(url, headers=headers, timeout=4).content
        title = ''.join(etree.HTML(html).xpath('//*[@id="post_head"]/h1/span[1]/span/text()'))
        if not title:
            title = ''.join(etree.HTML(html).xpath('//*[@id="container"]/div[2]/div[2]/h1/span/text()'))
        anwsers = etree.HTML(html).xpath('//div[@class="atl-main"]/div[@class="atl-item"]/div[2]/div[2]/div[1]/text()')
        if not anwsers:
            anwsers = etree.HTML(html).xpath('//div[@class="content"]/text()')
        # print(title)
        anwsers_new = [i.replace(" ", "").replace("\t", "").strip() for i in anwsers]
        dic = {
            'title': title,
            'anwsers': anwsers_new
        }
        col1.insert(dic)
        print(dic)
    except Exception as e:
        print(e)
        # get_detail(url)


def thread_main(item):
    pool = threadpool.ThreadPool(1)
    tasks = threadpool.makeRequests(get_detail, item)
    [pool.putRequest(req) for req in tasks]
    pool.wait()


def multipro_main(item):
    pool = multiprocessing.Pool(4)
    pool.map(get_detail, item)
    pool.close()


def thread():
    task = []
    for _ in range(1, 5):
        task.append(threading.Thread(target=get_detail))
    for t in task:
        t.start()
    for t in task:
        t.join()


if __name__ == '__main__':
    start_url = 'http://bbs.tianya.cnjavascript:history.go(-1)'
    add_bloom_from_mongo()
    # start_url = input('inout url: ')
    get_list(start_url, ls)

# http://bbs.tianya.cn/list-free-1.shtml 0
# http://bbs.tianya.cn/list-university-1.shtml 0 我的大学
# http://bbs.tianya.cn/list-828-1.shtml 1 百姓杂谈2
# http://bbs.tianya.cn/list-develop-1.shtml  经济
# http://bbs.tianya.cn/list-stocks-1.shtml 股票
# http://bbs.tianya.cn/list-1151-1.shtml 网络股
# http://bbs.tianya.cn/list-culture-1.shtml 文墨 ---
# http://bbs.tianya.cn/list-665-1.shtml 视频 ---
# http://bbs.tianya.cn/list-feeling-1.shtml 情感---
# http://bbs.tianya.cn/list-no11-1.shtml 时尚--
# http://bbs.tianya.cn/list-play-1.shtml 游戏--
# http://bbs.tianya.cn/list-lookout-1.shtml 了望天涯--
# http://bbs.tianya.cn/list-137-1.shtml  天香赌坊 
# http://bbs.tianya.cn/list-174-1.shtml 天涯志    2296638
# http://bbs.tianya.cn/list-810-1.shtml 天涯共此时 over
# http://bbs.tianya.cn/list-409-1.shtml 天涯玫瑰园 
# http://bbs.tianya.cn/list-172-1.shtml 天涯居委会 
# http://bbs.tianya.cn/list-410-1.shtml 主播 
# http://bbs.tianya.cn/list-168-1.shtml 天涯有我 
# http://bbs.tianya.cn/list-31-1.shtml 大话天涯 
# http://bbs.tianya.cn/list-411-1.shtml 天涯交易所 on--
