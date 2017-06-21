import numpy as np

# weight = [65.4, 59.2, 63.6, 88.4, 68.7]  #体重列表
# height = [1.73, 1.68, 1.71, 1.89, 1.79]  #身高列表
#
# np_height = np.array(height)
# np_weight = np.array(weight)
# bmi = np_weight / np_height ** 2
#
# print(bmi>20)


# 创建棒球运动员的身高列表 baseball
# baseball = [180, 215, 210, 210, 188, 176, 209, 200]
# np_baseball = np.array(baseball)
# print(type(np_baseball))
# high = np_baseball/100
# print(high)

# 找出高于2米的运动员身高数据
# print(high[high > 2])
# 打印输出最后一个棒球运动员的身高
# print(np_baseball[-1])
# 打印输出最后两个运动员的身高
# print(np_baseball[-2:])


# 创建二维列表 baseball, 第一列是身高，第二列是体重
baseball = [[180, 78.4],
            [215, 102.7],
            [210, 98.5],
            [188, 75.2]]

# 用二维列表baseball创建二维数组 np_baseball
np_baseball = np.array(baseball)
# 打印输出 np_baseball 的类型
print(type(np_baseball))
# 打印输出 np_baseball的shape属性
print(np_baseball.shape)
# 打印输出第3行的数据
print(np_baseball[2])
# 打印输出第二列体总数据
print(np_baseball[:, 1])
# 打印输出第4名运动员的身高
print(np_baseball[3][0])
print(np_baseball[3, 0])
