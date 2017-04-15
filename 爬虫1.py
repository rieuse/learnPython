import urllib.request
from bs4 import BeautifulSoup
import os
# 下载网页
url = 'http://jandan.net/ooxx/page-2397#comments'
res = urllib.request.urlopen(url)
html = res.read()
print(html)
# 解析网页
soup = BeautifulSoup(html, 'html.parser')
result = soup.find_all('img')
links = []
for content in result:
    links.append('http:' + content.get('src'))
# 下载并存储图片
if not os.path.exists('photo'):
    os.makedirs('photo')
i = 0
for link in links:
    i += 1
    filename = 'photo\\' + 'photo' + str(i) + '.png'
    with open(filename, 'w') as file:
        urllib.request.urlretrieve(link, filename)