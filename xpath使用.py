import urllib.request
from bs4 import BeautifulSoup
from lxml import etree

url = 'http://www.toutiao.com/a6402018208622510337/#p=1'
r = urllib.request.urlopen(url)
html = r.read().decode('utf-8')
# print(html)
selector = etree.HTML(html)
links = selector.xpath('/img')
for link in links:
    print (link)
