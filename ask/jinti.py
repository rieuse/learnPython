import json
import random
import redis
import requests
import threading
import threadpool
from lxml import etree
import pymongo
from bs4 import BeautifulSoup

clients = pymongo.MongoClient('localhost')
db = clients["ask"]
col = db["jinti"]

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
    # 'Cookie': 'ASP.NET_SessionId=1ougflfer4o204hj1mafg5y2; __utma=86209950.1130550908.1502336672.1502336672.1502336672.1; __utmb=86209950.6.10.1502336672; __utmc=86209950; __utmz=86209950.1502336672.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmt=1; visitList=267037,27249; __utma=47193788.1377076428.1502336710.1502336710.1502336710.1; __utmb=47193788.5.10.1502336710; __utmc=47193788; __utmz=47193788.1502336710.1.1.utmcsr=wenda.jinti.com|utmccn=(referral)|utmcmd=referral|utmcct=/l2n1s875z1.html',
    'User-Agent': random.choice(UA_LIST)
}

proxies = {
    'http': "http://HP59J4A78453575D:0306D55796F8EB59@http-dyn.abuyun.com:9020",
    'https': "http://HP59J4A78453575D:0306D55796F8EB59@http-dyn.abuyun.com:9020"
}


# def info_to_redis(data):
#     r = redis.StrictRedis(host='127.0.0.1',port=6379)
#     print("{} into redis".format(data))
#     r.rpush('rednet_url', data)
#
# def pop_from_redis():
#     r = redis.StrictRedis(host='127.0.0.1',port=6379, decode_responses=True)
#     return r.lpop('rednet_url')

def start(url):
    print(url)
    try:
        html = requests.get(url, headers=headers, proxies=proxies).text
        hrefs = etree.HTML(html).xpath('//*[@class="PwentiBox"]/div[1]/dl/dd/ul/li[1]/a/@href')
        main(hrefs)
        # for i in hrefs:
        #     print(i)
        #     # info_to_redis(i)
        #     with open('urls\\jinti_urls.txt', 'a') as f:
        #         f.write(i + '\n')
        #     # get(i)
        next_page = ''.join(etree.HTML(html).xpath('//*[@id="PageArea1"]/a[last()-1]/text()'))
        if '下一页' in next_page:
            u = 'http://wenda.jinti.com' + etree.HTML(html).xpath('//*[@id="PageArea1"]/a[last()-1]/@href')[0]
            start(u)
    except:
        start(url)


def get(url):
    try:
        html = requests.get(url, headers=headers, proxies=proxies).content.decode('utf-8')
        title = ''.join(etree.HTML(html).xpath('//*[@id="hasResult"]/div[1]/div[2]/div/h2/text()'))
        markitup = ''.join(etree.HTML(html).xpath('//*[@id="hasResult"]/div[1]/div[2]/div/p/text()'))
        comment = ''.join(etree.HTML(html).xpath('//*[@id="icomeansw"]/div[2]/div/div/div[1]/p/text()'))
        dic = {
            'title': title,
            'markitup': markitup,
            'comment': comment
        }
        col.insert(dic)
        with open('log\\log_jinti.txt', 'w') as f:
            f.write(url)
        print(title)
    except:
        get(url)


def main(item):
    pool = threadpool.ThreadPool(20)
    tasks = threadpool.makeRequests(get, item)
    [pool.putRequest(req) for req in tasks]
    pool.wait()


if __name__ == '__main__':
    start_url = 'http://wenda.jinti.com/l2n1s533z1.html'
    start(start_url)
