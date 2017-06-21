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
# np_baseball = np.array(baseball)
# 打印输出 np_baseball 的类型
# print(type(np_baseball))
# 打印输出 np_baseball的shape属性
# print(np_baseball.shape)
# 打印输出第3行的数据
# print(np_baseball[2])
# 打印输出第二列体总数据
# print(np_baseball[:, 1])
# 打印输出第4名运动员的身高
# print(np_baseball[3][0])
# print(np_baseball[3, 0])


# 综合练习：找出足球运动中守门员和其他运动员的身高的中位数。

# 创建足球运动员的位置和对应的身高数据
positions = ['GK', 'M', 'A', 'D', 'M', 'D', 'M', 'M', 'M', 'A', 'M', 'M', 'A', 'A', 'A', 'M', 'D', 'A', 'D', 'M', 'GK',
             'D', 'D', 'M', 'M', 'M', 'M', 'D', 'M', 'GK']
heights = [191, 184, 185, 180, 181, 187, 170, 179, 183, 186, 185, 170, 187, 183, 173, 188, 183, 180, 188, 175, 193, 180,
           185, 170, 183, 173, 185, 185, 168, 190]

# 将列表 positions 和 heights 分别转化成numpy数组: np_positions, np_heights
np_positions = np.array(positions)
np_heights = np.array(heights)
# 将守门员的身高数据存入变量 gk_heights， 守门员对应的位置编码是’GK‘
gk_heights = np_heights[np_positions == 'GK']  # 两次函数来取值
print(gk_heights)
# 将守门员之外的其他运动员的身高数据存入变量 other_heights
other_heights = np_heights[np_positions != 'GK']
print(other_heights)
# 打印输出守门员身高的中位数
print("Median height of goalkeepers: " + str(np.median(gk_heights)))

# 打印输出其他运动员身高的中位数
print("Median height of other players: " + str(np.median(other_heights)))
