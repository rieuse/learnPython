# 方法一：
# L = []
# n = 1
# while n <= 99:
#     L.append(n)
#     n = n + 4
# print(L[:(len(L)//2)])

# 方法二：
print([n for n in range(1, 99, 2) if n < len(range(1, 99, 2))])
