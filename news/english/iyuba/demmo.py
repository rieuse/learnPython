import requests

url = 'http://news.iyuba.com/essay/2017/09/28/58128.mp3'
with open('12', 'wb') as f:
    f.write(requests.get(url).content)
