import random
import requests
from lxml import etree
from bs4 import BeautifulSoup
import re

url = 'http://channel.chinanews.com/cns/s/channel:gj.shtml'
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Host': 'channel.chinanews.com',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
}
data = {
    'pager': '3',
    'pagenum': '20',
    # '_': '1500133135613'
}
s = requests.session()
cookies = s.get(url, params=data).cookies
for i, j in cookies.items():
    headers['Cookie'] = '__jsluid={}'.format(j)
html = s.get(url, params=data, headers=headers)
print(html.text)

# u = 'http://www.chinanews.com/m/gj/2017/07-16/8278878.shtml'
# html = requests.get(u).content.decode('utf-8')
# soup = BeautifulSoup(html,'lxml')
# print(soup.text)
