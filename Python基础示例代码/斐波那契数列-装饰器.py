import time


# 使用缓存来减少计算量
def fib(n, cache=None):
    if cache is None:
        cache = {}
    if n in cache:
        return cache[n]
    if n == 1 or n == 0:
        return 1
    else:
        cache[n] = fib(n - 2, cache) + fib(n - 1, cache)
        return cache[n]


start = time.time()
[fib(n) for n in range(999)]
end = time.time()

print('cost:{}'.format(end - start))

# 装饰器的斐波那契数列
start1 = time.time()


def decorate(func):
    cache = {}

    def wrap(n):
        if n not in cache:
            cache[n] = func(n)
        return cache[n]

    return wrap


@decorate
def fib2(n):
    if n == 1 or n == 0:
        return 1
    else:
        return fib2(n - 2) + fib2(n - 1)


end1 = time.time()
print([fib2(n) for n in range(0, 20)])

print('cost:{}'.format(end1 - start1))
