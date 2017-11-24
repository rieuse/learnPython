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
from bloomfilter_Redis import BloomFilter
import logging

sys.setrecursionlimit(1000000)

# config for logging
logger = logging.getLogger('log')
logger.setLevel(logging.INFO)

fh = logging.FileHandler('tinaya_log.txt')
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)
# logging.basicConfig(filename='tinaya_log.txt', format='%(asctime)s %(levelname)s：%(message)s',level=logging.INFO)
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
    # 'cookie': '_dacevid3=748ac4b3.2240.97e1.ca5d.3023e34efe24; _HUPUSSOID=5c904bc3-02a3-4c73-a630-1298ca6a354f; _CLT=b0c2a05996d8b48b354e1fa4ddfc1fef; u=32023008|5LiN6IKv5byA5Y+j|1068|568bcea6bff5398192f8e5c114a67672|bff5398192f8e5c1|aHVwdV9kMzQ2ZDdmNzc3M2RlZDIz; us=4a7ac4a0344d0f42cd093dbb393654f10e187dce817b6bc5b5f349c6de812ddc452edda81a76fd190ac22c90b1c10887af210b8718fe8b6ec2fc28ce3522bf02; _fmdata=4543AD30FB53502925A1CC1A227A8192C6419010310B679335F7B9CBF7FFC05EFDB446EED3ECF143E115FADEE69D04723488662B07B36DEC; ua=166995178; lastvisit=6699%091502956882%09%2Fthread.php%3Fboardname%3Dtopic%26page%3D2; __dacevst=390ffac6.37cb7c32|1502958681045; _cnzz_CV30020080=buzi_cookie%7C748ac4b3.2240.97e1.ca5d.3023e34efe24%7C-1; Hm_lvt_39fc58a7ab8a311f2f6ca4dc1222a96e=1502681042,1502681117,1502760900,1502956607; Hm_lpvt_39fc58a7ab8a311f2f6ca4dc1222a96e=1502956882'
}
clients = pymongo.MongoClient('localhost')
db = clients["bbs"]
col = db["tianya-bbs"]

proxies = {
    'http': "http://HW2XS2E6K7BA276D:9688CB7DA500A54D@http-dyn.abuyun.com:9020",
    'https': "http://HW2XS2E6K7BA276D:9688CB7DA500A54D@http-dyn.abuyun.com:9020"
}


def to_bloom(link):
    bf = BloomFilter()
    bf.insert(link)


def is_contains(link):
    bf = BloomFilter()
    return bf.isContains(link)


def get_list(url):
    print('this list url is :   ', url)
    if is_contains(url) == 0:
        # with open('tianya_ask_url_log.txt', 'w') as f:
        #     f.write(url)
        logger.info('URL:  ' + url)
        try:
            html = requests.get(url, headers=headers, timeout=4).content
        except requests.exceptions.ConnectionError:
            html = ''
            get_list(url)
        # print(html.decode('utf-8'))
        ls = etree.HTML(html).xpath(''
                                    '//*[@id="main"]/div[6]/table/tbody/tr/td[1]/a/@href')
        if not ls:
            ls = etree.HTML(html).xpath('//*[@id="main"]/div[7]/table/tbody/tr/td[1]/a/@href')
        detail_list = []
        for i in ls:
            link = 'http://bbs.tianya.cn' + i
            detail_list.append(link)
        thread_main(detail_list)
        # multipro_main(detail_list)
        to_bloom(url)
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
            get_list(next_link)
        except requests.exceptions.Timeout:
            print('error')
            print(next_link)
            # print(next_link)
            get_list(next_link)


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
        col.insert(dic)
        print(dic)
    except Exception as e:
        print(e)
        # get_detail(url)


def thread_main(item):
    pool = threadpool.ThreadPool(8)
    tasks = threadpool.makeRequests(get_detail, item)
    [pool.putRequest(req) for req in tasks]
    pool.wait()


def multipro_main(item):
    pool = multiprocessing.Pool(8)
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
    url = 'http://bbs.tianya.cn/list.jsp?item=free&nextid=1439476040000'
    get_list(url)
    # url = 'http://bbs.tianya.cn/post-907-15574-1.shtml'
    # get_detail(url)
    # print(is_contains('http://bbs.tianya.cn/list.jsp?item907&nextid=1490846995000'))
