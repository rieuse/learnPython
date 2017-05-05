import requests
import os
import PIL.Image
import PIL.p

url = 'http://my.hlju.edu.cn/captchaGenerate.portal?'
if not os.path.exists('yzm'):
    os.makedirs('yzm')
for i in range(1, 99):
    r = requests.get(url)
    name = 'img\\yzm\\' + str(i) + '.png'
    with open(name, 'wb') as fo:
        fo.write(r.content)
