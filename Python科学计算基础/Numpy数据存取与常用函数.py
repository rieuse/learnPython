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
