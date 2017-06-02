import pymongo
import pandas
import matplotlib.pyplot as plt

# 学习数据分析斗鱼房间信息

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

client = pymongo.MongoClient('localhost')
db = client["DouyuTV"]
room = db["Roominfo"]
# 使用pandas作图

# data = pandas.DataFrame(list(room.find()))
# del data['_id'], data['room_src'],data['vertical_src'],data['isVertical']  #去除不需要的数据
# data = data[['room_id', 'nickname', 'online', 'fans']]  # 取得我们指定需要的数据
data = room.find()
nickname = []
online = []
for i in data:
    nickname.append(i['nickname'])
    online.append(i['online'])
plt.plot(online, online, color='green', marker='o', linestyle='solid')
plt.title(u'douyuTV人气值')
plt.ylabel('人气')
plt.show()
