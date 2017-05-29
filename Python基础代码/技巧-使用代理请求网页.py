import requests

proxies = {
    # "http": "http://218.201.98.196:3128",
    "https": "http://218.201.98.196:3128",
}
r = requests.get("https://httpbin.org/ip", proxies=proxies)
html = r.text
print(html)


# 代理池  http://7xrnwq.com1.z0.glb.clouddn.com/proxy_list.txt
# 代理池 http://api.xicidaili.com/free2016.txt

# request = requests.get('http://7xrnwq.com1.z0.glb.clouddn.com/proxy_list.txt')
# print(request.text)
