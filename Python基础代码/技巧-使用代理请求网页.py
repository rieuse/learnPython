import requests
from bs4 import BeautifulSoup

# proxies = {
#     'https': '123.206.6.17:443'
# }
# r = requests.get("http://www.ip.cn/", proxies=proxies)
# soup = BeautifulSoup(r.text, 'lxml')
# print(r.text)


# 代理池  http://7xrnwq.com1.z0.glb.clouddn.com/proxy_list.txt
# 代理池 http://api.xicidaili.com/free2016.txt

# request = requests.get('http://7xrnwq.com1.z0.glb.clouddn.com/proxy_list.txt')
# print(request.text)


ss = requests.session()

ss.proxies = {'http': 'http://123.206.6.17:3128', 'https': 'http://123.206.6.17:3128'}

print(ss.get('http://www.qq.com'))
print(ss.get('https://www.github.com'))
