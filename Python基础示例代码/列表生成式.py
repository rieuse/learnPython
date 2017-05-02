# 生成[1x1, 2x2, 3x3, ..., 10x10]
print([x * x for x in range(1, 11)])
# 可以使用两层循环，可以生成全排列
print([m + n for m in 'ABC' for n in 'XYZ'])

import os

print([d for d in os.listdir('.')])
