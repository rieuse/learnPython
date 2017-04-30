# -*-coding:utf-8-*-
import csv
import requests
from bs4 import BeautifulSoup

base_url = 'http://www.jianshu.com/trending/weekly'
r = requests.get(base_url)
html = r.text
soup = BeautifulSoup(html, 'html.parser')
articles = []
for article in soup.find_all(class_='content'):
    title = article.find(class_='title').get_text()
    link = 'http://www.jianshu.com' + article.find(class_='title').get('href')
    author = article.find(class_='blue-link').string
    time = article.span['data-shared-at']
    meta = article.find(class_='meta').find_all(['a', 'span'])
    metas = []
    for item in meta:
        metas.append(item.get_text().strip())
    read = metas[0]
    comment = metas[1]
    like = metas[2]
    try:
        money = metas[3]
    except:
        money = None
    articles.append([title, author, time, read, comment, like, money, link])

data_list = []
for i in range(1, 7):
        url = base_url + '?page={}'.format(i)
        data = articles
        data_list.append(data)

with open('jianshu2.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['文章标题', '作者', '时间', '阅读量', '评论', '喜欢', '赞赏数', '文章地址'])
    for data in data_list:
        for row in data:
            writer.writerow(row)