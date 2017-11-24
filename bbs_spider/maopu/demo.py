import re

import pymongo

clients = pymongo.MongoClient('localhost')
db = clients["bbs"]
col1 = db["maopu33"]

# id = list(col1.find())[-1]['startcol']
# print(id)

with open('maopu.log', 'r') as f:
    line = f.readlines()[-1]
    print(line)
    start = re.findall('(?<=pgnum=)\d*(?=&colid)', line)
    print(start)
