import urllib.request
from bs4 import BeautifulSoup
import os
# 下载网页
url = 'http://www.yidianzixun. com/home?page=article&id=0G5zThN8&up=0'
res = urllib.request.urlopen(url)
html = res.read().decode('utf-8')
# 解析网页
soup = BeautifulSoup(html, 'html.parser')
result = soup.find_all('img',limit=10)
links = []
for content in result:
    links.append(content.get('src'))
# 下载并存储图片
if not os.path.exists('photo'):
    os.makedirs('photo')
i = 0
for link in links:
    i += 1
    filename = 'photo\\' + 'photo' + str(i) + '.gif'
    with open(filename, 'w') as file:
        urllib.request.urlretrieve(link, filename)