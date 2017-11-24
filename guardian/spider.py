from pprint import pprint
import requests
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6'}


def crawl():
    url = 'http://www.ximalaya.com/tracks/57774592.json'
    data = requests.get(url, headers=headers).json()
    # pprint(data)
    while True:
        for i in range(99999999):
            num = i ** i
            num = num ** num
            # print(num)
            # for i,j in data.items():
            #     print()
            #     time.sleep(2)


if __name__ == '__main__':
    crawl()
