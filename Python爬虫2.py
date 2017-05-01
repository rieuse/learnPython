import urllib.request
from bs4 import BeautifulSoup
import os

url = 'http://www.8she.com/31988.html'
res = urllib.request.urlopen(url)
html = res.read().decode('utf-8')
soup = BeautifulSoup(html, 'html.parser')
result = soup.find_all(class_='aligncenter', limit=15)
# print(result)
links = []
for content in result:
    links.append(content.get('src'))
# 下载并存储图片
if not os.path.exists('E:\\rieuse\爬虫图片\photo2'):
    os.makedirs('E:\\rieuse\爬虫图片\photo2')
i = 0
for link in links:
    i += 1
    filename = 'E:\\rieuse\爬虫图片\photo2\\' + 'photo' + str(i) + '.jpg'
    with open(filename, 'w') as file:
        urllib.request.urlretrieve(link, filename)
