import requests
from bs4 import BeautifulSoup
import time
import ws4py
from ws4py.websocket import WebSocket
from ws4py.client.threadedclient import WebSocketClient

host = 'http://yyweb.yystatic.com'
url1 = 'http://wap.yy.com'
url2 = 'http://wap.yy.com/mobileweb/54880976/54880976?u=147125102'
url3 = 'http://175.20.85.16:493/54880976_54880976_150130800_0_0_15013.m3u8?uuid=9476b0f697ba4cd7aa1959f790a825a3&org=yyweb&m=677b0b8b4afa29bb0aff6152b0a2e7b9&r=1396616476&v=1&t=1497363682&uid=0&ex_audio=0&ex_coderate=700&ex_spkuid=0'
url4 = 'http://q.m.yy.com/datasource_web/collect.action'
url5 = 'ws://tvgw.yy.com:26101/websocket'
headers1 = {
    'Upgrade-Insecure-Requests': '1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; SM919 Build/MXB48T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.84 Mobile Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,en-US;q=0.8',
    'Cookie': 'hiido_ui=0.4971752367014193; JSESSIONID=01692C3162F29761EDBC49EF6A477A25; Hm_lvt_8e2de05488f2c880d285705bb169c6b1=1497343105,1497345711,1497361943,1497361966; Hm_lpvt_8e2de05488f2c880d285705bb169c6b1=1497362916',
    'If-Modified-Since': 'Tue, 13 Jun 2017 14:08:33 GMT'
}
headers2 = {
    'Upgrade-Insecure-Requests': '1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Referer': 'http://wap.yy.com/',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; SM919 Build/MXB48T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.84 Mobile Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,en-US;q=0.8',
    'Cookie': 'hiido_ui=0.4971752367014193; JSESSIONID=01692C3162F29761EDBC49EF6A477A25; Hm_lvt_8e2de05488f2c880d285705bb169c6b1=1497343105,1497345711,1497361943,1497361966; Hm_lpvt_8e2de05488f2c880d285705bb169c6b1=1497362916',
    'If-Modified-Since': 'Tue, 13 Jun 2017 14:08:33 GMT'
}
headers3 = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; SM919 Build/MXB48T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.84 Mobile Safari/537.36',
    # 'Cookie': 'user=TestCookie',
    'allow-cross-domain-redirect': 'false',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
    'Cookie': '$Version="1"; user="TestCookie";$Path="/";$Domain="175.20.85.16"',
}
headers4 = {
    'Content-Length': '596',
    'Cache-Control': 'max-age=0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Origin': 'http://wap.yy.com',
    'User-Agent': 'Mozilla/5.0 (Linux; U; Android 6.0.1; zh-CN; SM919 Build/MXB48T) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 Quark/1.7.2.917 Mobile Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': 'http://wap.yy.com/mobileweb/54880976/54880976?u=1538324096',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,en-US;q=0.8',
    'Cookie': 'hiido_ui=0.9239800956565887'
}
headers5 = {
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Upgrade': 'websocket',
    'Connection': 'Upgrade',
    'Origin': 'http://wap.yy.com',
    'Sec-WebSocket-Version': '13',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,en-US;q=0.8',
    'Cookie': 'hiido_ui=0.9694292733911425',
    'User-Agent': 'Mozilla/5.0 (Linux; U; Android 6.0.1; zh-CN; SM919 Build/MXB48T) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 Quark/1.7.2.917 Mobile Safari/537.36',
    'Sec-WebSocket-Key': 'QqUKb4fjHIAfCjo7HgfgBA==',
    'Sec-WebSocket-Extensions': 'permessage-deflate; client_max_window_bits'
}


def ss(url, headers):
    s = requests.session()
    r = s.get(url, headers=headers)
    # soup = BeautifulSoup(r.text, 'lxml')
    # print(soup.prettify())
    time.sleep(1)
    print('---------------进行下一步---------------')


ss(url1, headers1)
ss(url2, headers2)
ss(url3, headers3)


class DummyClient(WebSocketClient):
    def opened(self):
        self.send("1")

    def closed(self, code, reason=None):
        print("Closed down", code, reason)

    def received_message(self, m):
        print(m)


if __name__ == '__main__':
    ws = DummyClient(url5, protocols=['chat'])
    try:
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()
