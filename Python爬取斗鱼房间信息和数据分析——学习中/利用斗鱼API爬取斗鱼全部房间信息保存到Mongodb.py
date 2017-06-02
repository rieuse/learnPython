import json

import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost')
db = client["DouyuTV"]
col = db["Roominfo"]
host = 'http://api.douyutv.com/api/v1/live/'
all_game = 'http://open.douyucdn.cn/api/RoomApi/game'
sort = []


def parser(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    jn = json.loads(soup.text)
    return jn


def get_room_sort(url):
    jn = parser(url)
    data = jn['data']
    for item in data:
        sort.append(host + item['short_name'])


def get_room_info():
    for item in sort:
        jn = parser(item)
        data = jn['data']
        try:
            col.insert(data)
        except Exception as e:
            pass


if __name__ == '__main__':
    get_room_sort(all_game)
    get_room_info()
