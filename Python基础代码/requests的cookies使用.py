import requests
from bs4 import BeautifulSoup

url = 'http://www.imooc.com/u/2379448'
coo = 'imooc_uuid=8062f183-5579-4e63-bf43-528db6f24e61; imooc_isnew_ct=1492831625; PHPSESSID=oohki1kib5vfua4mhhr4aalmf6; loginstate=1; apsid=U5M2NlNWJmOGU4ODY5YjJlYTkxZjEwMzIzOTc5Y2UAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMjM3OTQ0OAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGU2ZGJjYWVmMjVkYTNlYjRkMDIwM2ZiMzc4ZjM5NDY5CZ8EWQmfBFk%3DNj; IMCDNS=0; imooc_isnew=2; cvde=59049de1aa803-72'
cookies = {}
for content in coo.split(';'):
    name, value = coo.split('=', 1)
    cookies[name] = value
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
r = requests.get(url, headers=headers, cookies=cookies)
html = r.text
soup = BeautifulSoup(html, 'html.parser')
print(r.headers)
