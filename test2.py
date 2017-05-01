# -*-coding:utf-8-*-
import csv
import requests
from bs4 import BeautifulSoup

base_url = 'http://www.jianshu.com/trending/weekly'

articles = []
data_list = []
for i in range(1, 7):
    url = base_url + '?page={}'.format(i)
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, 'html.parser')
    for article in soup.find_all(class_='content'):
        title = article.find(class_='title').get_text()
        link = 'http://www.jianshu.com' + article.find(class_='title').get('href')
        author = article.find(class_='blue-link').get_text()
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
            money = '0'
        articles.append([title, author, time, read, comment, like, money, link])

with open('jianshu.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['文章标题', '作者', '时间', '阅读量', '评论', '喜欢', '赞赏数', '文章地址'])
    for row in articles:
        writer.writerow(row)