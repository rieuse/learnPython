"""本次的练习目的：掌握表示、清洗、统计和展示数据的能力"""
import numpy as np

"""
数据的CSV文件存取
"""
# np.savetxt(frame, array, fmt='%.18e', delimiter=None)
# • frame : 文件、字符串或产生器，可以是.gz或.bz2的压缩文件
# • array : 存入文件的数组
# • fmt : 写入文件的格式，例如：%d %.2f %.18e
# • delimiter : 分割字符串，默认是任何空格

# a1 = np.arange(100).reshape(5, 20)
# np.savetxt('a1.csv', a1, fmt = '%d', delimiter=',')
#
# a2 = np.arange(100).reshape(5, 20)
# np.savetxt('a2.csv', a2, fmt = '%.1f', delimiter=',')

# np.loadtxt(frame, dtype=np.float, delimiter=None， unpack=False)
# • frame : 文件、字符串或产生器，可以是.gz或.bz2的压缩文件
# • dtype : 数据类型，可选
# • delimiter : 分割字符串，默认是任何空格
# • unpack  : 如果True，读入属性将分别写入不同变量

# b1 = np.loadtxt('a1.csv', delimiter=',')
# print(b1)
# b2 = np.loadtxt('a2.csv', dtype=np.int, delimiter=',')
# print(b2)

'''CSV只能有效存储一维和二维数组,np.savetxt() np.loadtxt()只能有效存取一维和二维数组'''

"""
多维数据的存取(字符串与二进制的数据写入读取)
"""
# 二进制更节省储存空间 这个和编码有关系

# a.tofile(frame, sep='', format='%s')
# • frame  : 文件、字符串
# • sep : 数据分割字符串，如果是空串，写入文件为二进制
# • format : 写入数据的格式

# a = np.arange(100).reshape(5, 10, 2)
# a.tofile('b.dat', sep=',', format='%d')
# a.tofile('c.bat', format='%d')


# np.fromfile(frame, dtype=float, count=‐1, sep='')
# • frame  : 文件、字符串
# • dtype : 读取的数据类型
# • count  : 读入元素个数，‐1表示读入整个文件
# • sep : 数据分割字符串，如果是空串，写入文件为二进制

# a1 = np.fromfile('b.dat', dtype=np.int, sep=',').reshape(5, 10, 2)
# print(a1)
# a2 = np.fromfile('c.bat', dtype=np.int).reshape(5, 10, 2)
# print(a2)

'''
注意事项：
该方法需要读取时知道存入文件时数组的维度和元素类型
a.tofile()和np.fromfile()需要配合使用
可以通过元数据文件来存储额外信息
'''

"""
numpy的便捷文件存取
"""

# np.save(fname, array) 或 np.savez(fname, array)
# • fname : 文件名，以.npy为扩展名，压缩扩展名为.npz
# • array  : 数组变量
# np.load(fname)
# • fname : 文件名，以.npy为扩展名，压缩扩展名为.npz

a = np.arange(100).reshape(5, 10, 2)
np.save('a.npy', a)
