def triangles():
    g = [1]
    while True:
        yield g
        g.append(0)
        g = [g[i] + g[i - 1] for i in range(len(g))]


# 方法二
# def Triangles():
#     L = [1]
#     while True:
#         yield L
#         L = [1] + [L[i-1]+L[i] for i in range(len(L)) if i>0] + [1]
n = 0
for t in triangles():
    print(t)
    n = n + 1
    if n == 10:
        break
