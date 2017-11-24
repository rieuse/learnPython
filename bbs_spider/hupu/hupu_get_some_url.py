import requests
from lxml import etree

url1 = 'https://bbs.hupu.com/get_nav?fup=1'
data = requests.get(url1).json()
album_urls = ['https:' + i['url'] for i in data['data']]
print(album_urls)
