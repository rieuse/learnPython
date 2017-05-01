import requests

proxies = {
    "http": "http://123.206.6.17:90",
    "https": "http://123.206.6.17:90",
}
r = requests.get("http://httpbin.org/ip", proxies=proxies)
html = r.text
print(html)
