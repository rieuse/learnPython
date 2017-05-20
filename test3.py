import requests

url = 'http://huaban.com/favorite/beauty/'
params = {
    'j0ga0hbi': '',
    'max': '1062161596',
    'limit': '100',
    'wfl': '1'
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Accept': 'application/json',
    'X-Request': 'JSON',
    'X-Requested-With': 'XMLHttpRequest'
}
html = requests.get(url=url, params=params, headers=headers)
print(html.text)
