'''
通过列表生成式，我们可以直接创建一个列表。但是，受到内存限制，
列表容量肯定是有限的。而且，创建一个包含100万个元素的列表，
不仅占用很大的存储空间，如果我们仅仅需要访问前面几个元素，
那后面绝大多数元素占用的空间都白白浪费了。所以，
如果列表元素可以按照某种算法推算出来，
那我们是否可以在循环的过程中不断推算出后续的元素呢？
这样就不必创建完整的list，从而节省大量的空间。
在Python中，这种一边循环一边计算的机制，称为生成器：generator。
要创建一个generator，第一种方法很简单，只要把一个列表生成式的[]改成()
'''

# 生成器的唯一注意事项就是：生成器只能遍历一次。
g = (x * x for x in range(10))
print(g)
for n in g:
    print(n)
# 我们创建了一个generator后，基本上永远不会调用next()，
# 而是通过for循环来迭代它，并且不需要关心StopIteration的错误。


# 打印9*9乘法表
def table_9_9(max=9):
    n = 1
    while n <= max:
        N = ['{}*{}={}'.format(i, n, n * i) for i in range(1, n + 1)]
        n += 1
        yield N


T = table_9_9()
for t in T:
    print(t)


# 斐波那契数列
def fab(max):
    n, a, b = 0, 0, 1
    list = []
    for i in range(max):
        list.append(b)
        yield list
        a, b = b, a + b


for n in fab(7):
    print(n)


# 杨辉三角
def triangle(max):
    N = [1]
    n = 0
    while n < max:
        yield N
        N.append(0)
        N = [N[i - 1] + N[i] for i in range(len(N))]
        n += 1


for t in triangle(10):
    print(t)

'''
对于生成器还有一些send(),close()和throw()方法，特别是send()不仅可以传值给yield，还能恢复生成器，大大简化协同程序的实现
'''
