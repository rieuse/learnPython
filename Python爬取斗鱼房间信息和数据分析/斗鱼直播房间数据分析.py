import pymongo
import pandas
import matplotlib.pyplot as plt

client = pymongo.MongoClient('localhost')
db = client["DouyuTV"]
room = db["Roominfo"]
data = pandas.DataFrame(list(room.find()))
# del data['_id'], data['room_src'],data['vertical_src'],data['isVertical']  #去除不需要的数据
data = data[['room_id', 'nickname', 'online', 'fans']]  # 取得我们指定需要的数据
l = list(data)
print(l)
print(type(l))
name = data['nickname']
online = data['online']


# plt.plot(name,online,color='green',marker='o',linestyle='solid')
# plt.title('小试牛刀')
# plt.ylabel('people')
