import numpy as np

"""
创建ndarray数组

"""
# Method 1: 基于list或tuple
# 一维数组
#
# 基于list
# arr1 = np.array([1,2,3,4])
# print(arr1)
#
# 基于tuple
# arr_tuple = np.array((1,2,3,4))
# print(arr_tuple)
#
# 二维数组 (2*3)
# arr2 = np.array([[1,2,4], [3,4,5]])
# print(arr2)
#
# Method 2: 基于np.arange
# 一维数组
# arr1 = np.arange(5)
# print(arr1)
#
# 二维数组
# arr2 = np.array([np.arange(3), np.arange(3)])
# print(arr2)
#
# Method 3: 基于arange以及reshape创建多维数组
# 创建三维数组
# arr = np.arange(24).reshape(2,3,4)
# print(arr)
'''请注意：arange的长度与ndarray的维度的乘积要相等，即 24 = 2X3X4'''

'''ndarray数组的属性'''
# np.arange(4, dtype=float)

# # 'D'表示复数类型
# np.arange(4, dtype='D')
# np.array([1.22,3.45,6.779], dtype='int8')

# ndim属性，数组维度的数量
# a = np.array([[1,2,3], [7,8,9]])
# print(a.ndim)

# shape属性，数组对象的尺度，对于矩阵，即n行m列,shape是一个元组（tuple）
# print(a.shape)

# size属性用来保存元素的数量，相当于shape中nXm的值
# print(a.size)

# itemsize属性返回数组中各个元素所占用的字节数大小。
# print(a.itemsize)

# nbytes属性，如果想知道整个数组所需的字节数量，可以使用nbytes属性。其值等于数组的size属性值乘以itemsize属性值。
# print(a.nbytes)
# print(a.size*a.itemsize)

# T属性，数组转置
# b = np.arange(24).reshape(4,6)
# print(b.T)

# 复数的实部和虚部属性，real和imag属性
# d = np.array([1.2+2j, 2+3j])
# real属性返回数组的实部
# print(d.real)
# imag属性返回数组的虚部
# print(d.imag)

# flat属性，返回一个numpy.flatiter对象，即可迭代的对象。
# e = np.arange(6).reshape(2,3)
# f = e.flat
# for item in f:
#     print(item)
# 可通过位置进行索引，如下：

# print(f[2])
# print(f[[1,4]])
# 也可以进行赋值
# e.flat=7
# e.flat[[1,4]]=1


"""ndarray数组的切片和索引"""
# 一维数组的切片和索引与python的list索引类似。
# 二维数组的切片和索引:1轴方向向右，0轴方向向下



"""处理数组形状"""
'''形状转换'''
'''函数resize（）的作用跟reshape（）类似，但是会改变所作用的数组，相当于有inplace=True的效果'''
a = np.arange(12).reshape(4, 3)
# print(a.reshape(3,4))
# print(a)
# print(a.resize(6,2))
# print(a)
#
# print(b.ravel())

# 用tuple指定数组的形状，如下：
# a.shape=(2,6)


'''ravel()和flatten()，将多维数组转换成一维数组，如下：
两者的区别在于返回拷贝（copy）还是返回视图（view），flatten()返回一份拷贝，
需要分配新的内存空间，对拷贝所做的修改不会影响原始矩阵，
而ravel()返回的是视图（view），会影响原始矩阵。
'''
# b = np.arange(12).reshape(4,3)
# b.ravel()
# b.ravel()[2]=10
# print(b)
# b.flatten()[2]=15
# print(b)


'''转置'''
# b = np.arange(12).reshape(4,3)
# print(b.transpose())

'''堆叠数组'''
# b = np.arange(12).reshape(4,3)
# print(b*2)

'''水平叠加hstack()'''
# b = np.arange(12).reshape(4,3)
# c = b*2
# print(b)
# print(c)
# print(np.hstack((b,c)))
# column_stack()函数以列方式对数组进行叠加，功能类似hstack（）
# print(np.column_stack((b,c)))


'''垂直叠加vstack()'''
# b = np.arange(12).reshape(4,3)
# c = b*2
# print(b)
# print(c)
# print(np.vstack((b,c)))
# row_stack()函数以行方式对数组进行叠加，功能类似vstack（）
# print(np.row_stack((b,c)))


'''concatenate()方法，通过设置axis的值来设置叠加方向'''
# axis=1时，沿水平方向叠加
# axis=0时，沿垂直方向叠加

# b = np.arange(12).reshape(4,3)
# c = b*2
# print(np.concatenate((b,c),axis=1))
# print(np.concatenate((b,c),axis=0))


'''深度叠加'''
# b = np.arange(12).reshape(2,6)
# c = b*2
# print(b)
# print(c)
# print('----------------------')
# arr_dstack = np.dstack((b,c))
# print(arr_dstack.shape)
# print(np.dstack((b,c)))




'''数组的拆分'''
# 跟数组的叠加类似，数组的拆分可以分为横向拆分、纵向拆分以及深度拆分。
# 涉及的函数为 hsplit()、vsplit()、dsplit() 以及split()
# b = np.arange(12).reshape(2,6)

# 沿横向轴拆分（axis=1）
# print(np.hsplit(b, 3))
# print(np.split(b,2, axis=1))

# 沿纵向轴拆分（axis=0）
# print(np.vsplit(b, 2))
# print(np.split(b,2,axis=0))



'''深度拆分'''
# 拆分的结果是原来的三维数组拆分成为两个二维数组。
# b = np.arange(12).reshape(2,3,2)
# print(np.dsplit(b,2))




""""数组的类型转换"""
# 数组转换成list，使用tolist() 不会改变原来的numpy数组
# b = np.arange(12).reshape(2, 6)
# print(b.tolist())
# print(type(b.tolist()))

# 转换成指定类型，astype()函数
# print(b.astype(float))



"""numpy常用统计函数"""
# 请注意函数在使用时需要指定axis轴的方向，若不指定，默认统计整个数组。

# np.sum()，返回求和
# np.mean()，返回均值

# np.max()，返回最大值
# print(np.max(b))
# 沿axis=1轴方向统计
# np.max(b,axis=1)
# 沿axis=0轴方向统计
# np.max(b,axis=0)

# np.min()，返回最小值
# print(np.min(b))

# np.ptp()，数组沿指定轴返回最大值减去最小值，即（max-min）
# print(np.ptp(b))

# np.std()，返回标准偏差（standard deviation）
# np.var()，返回方差（variance）

# np.cumsum()，返回累加值
# print(np.cumsum(b, axis=1))

# np.cumprod()，返回累乘积值
# print(np.cumprod(b,axis=1))
# print(np.cumprod(b,axis=0))



"""数组的广播"""
# 当数组跟一个标量进行数学运算时，标量需要根据数组的形状进行扩展，然后执行运算。
# 这个扩展的过程称为“广播（broadcasting）”

# b = np.arange(12).reshape(2, 6)
# d = b + 2
# print(d)





""""一些简单练习"""

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
