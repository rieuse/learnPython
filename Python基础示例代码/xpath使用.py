import urllib.request
from bs4 import BeautifulSoup
from lxml import etree
import os

url = 'http://www.toutiao.com/a6402018208622510337/#p=1'
r = urllib.request.urlopen(url)
html = r.read().decode('utf-8')
# print(html)
selector = etree.HTML(html)
# result = etree.tostring(selector,pretty_print=True)
# print(result)
links = selector.xpath('//*[@id="header"]/div[2]/div/div[1]/a/img')
print(links)
print(type(links))
if not os.path.exists('xpath'):
    os.makedirs('xpath')
i = 0
for link in links:
    i += 1
    filename = 'xpath\\' + 'xpath' + str(i) + '.png'
