import urllib.request
import json
import requests
from collections import OrderedDict

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
}
# 实例一：

# url = 'http://www.weather.com.cn/data/cityinfo/101050101.html'
# r= requests.get(url)
# html = r.content.decode('utf-8')
# dic = json.loads(html)
# we = dic['weatherinfo']
# print('城市：'+ we['city'])
# print('时间：'+we['ptime'])
# print('天气：'+we['weather'])
# print('最高温度：'+we['temp2'])
# print('最低温度：'+we['temp1'])

# 实例二：
url2 = 'http://www.zimuzu.tv/public/hotkeyword'
r2 = requests.get(url2, headers=headers)
html2 = r2.content.decode('utf-8')
dict = json.loads(html2, object_pairs_hook=OrderedDict)
u = []
for i in range(0, 10):
    k = dict['data'][i]['keyword']
    u.append(k)
print(u)
