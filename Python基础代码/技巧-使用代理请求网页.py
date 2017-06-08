import requests
from bs4 import BeautifulSoup

# 测试代理的示例1
proxies = {
    'http': '115.127.77.10:80'
}
r = requests.get("http://icanhazip.com/", proxies=proxies)  # http://httpbin.org/ip也可以
print(r.text)
# r2 = requests.get('http://httpbin.org/get?show_env=1', proxies=proxies)
# print(r2.text)

# 访问 http://httpbin.org/get?show_env=1 ，得到访问头的详细信息，判断代理的匿名程度。
# 代理池  http://7xrnwq.com1.z0.glb.clouddn.com/proxy_list.txt
# 代理池 http://api.xicidaili.com/free2016.txt

# request = requests.get('http://7xrnwq.com1.z0.glb.clouddn.com/proxy_list.txt')
# print(request.text)

# 测试代理的示例2
# ss = requests.session()
# ss.proxies = {'http': 'http://123.206.6.17:3128', 'https': 'http://123.206.6.17:3128'}
# print(ss.get('http://www.qq.com'))
# print(ss.get('https://www.github.com'))
