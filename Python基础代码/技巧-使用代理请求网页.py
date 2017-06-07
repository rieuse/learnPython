import requests
from bs4 import BeautifulSoup


proxies = {
    'http': '123.206.6.17:808'
}
r = requests.get("http://www.ip.cn/", proxies=proxies)
soup = BeautifulSoup(r.text, 'lxml')
print(r.text)


# 代理池  http://7xrnwq.com1.z0.glb.clouddn.com/proxy_list.txt
# 代理池 http://api.xicidaili.com/free2016.txt

# request = requests.get('http://7xrnwq.com1.z0.glb.clouddn.com/proxy_list.txt')
# print(request.text)
