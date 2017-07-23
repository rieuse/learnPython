import requests
import time

for i in range(1, 1001):
    with open('img\\{}.png'.format(i), 'wb') as f:
        time.sleep(0.1)
        f.write(requests.get('http://my.hlju.edu.cn/captchaGenerate.portal').content)
        print('成功获取一张验证码')
