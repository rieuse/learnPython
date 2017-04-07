# -*- coding: utf-8 -*-
import requests
r = requests.get("https://github.com")
r.status_code
r.encoding = 'utf-8'
print(r.text)
