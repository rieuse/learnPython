import requests
from bs4 import BeautifulSoup
import pymongo
import time

clients = pymongo.MongoClient('localhost')
db = clients["wandoujia"]
col = db["info"]

start = time.time()
urls = ['http://www.wandoujia.com/award?page={}'.format(num) for num in range(1, 46)]
for url in urls:
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    title = soup.find_all(class_='title')
    app_title = soup.find_all(class_='app-title')
    item_cover = soup.find_all(class_='item-cover')
    icon_cover = soup.select('div.list-wrap > ul > li > div.icon > img')
    for title_i, app_title_i, item_cover_i, icon_cover_i in zip(title, app_title, item_cover, icon_cover):
        content = {
            'title': title_i.get_text(),
            'app_title': app_title_i.get_text(),
            'item_cover': item_cover_i['data-original'],
            'icon_cover': icon_cover_i['data-original']
        }
        col.insert(content)
        print('插入成功一组数据' + str(content))

print('一共用时：' + str(time.time() - start))
