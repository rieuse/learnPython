# def decorator(func):
#     def wrapped():
#         print("{} is running".format(func.__name__))
#         return func()
#
#     return wrapped
#
#
# def foo():
#     print("I'm the function")
#
#
# wrapped_func = decorator(foo)
# wrapped_func()
#
#
# @decorator
# def bar():
#     print("I'm the man")
#
#
# bar()
def outer(function):
    def inner():
        print("执行function之前可以进行额外操作")
        result = function()
        print("执行function之后还可以进行额外操作")
        result *= 2  # 对function的返回值本身进行额外操作
        return result  # 返回‘加强’后的结果

    return inner


def wait_for_deco():
    return 1024


decorated = outer(wait_for_deco)
print(decorated())


# 使用装饰器
@outer
def wait_for_deco():
    return 1024


print(wait_for_deco())


# 例如为下面的函数写一个装饰器，应该在内部的wapper中按原样传递参数
def decorator(func):
    def wrapper(x, y):
        ret = func(x, y)  # 原函数的返回值
        return ret * 2  # 原函数的结果“加强”后再返回

    return wrapper


@decorator
def wait_for_deco(x, y):
    return x + y


print(wait_for_deco(1, 2))


# 原函数有x, y, z三个参数，把结果放大两倍的装饰器
def decorator(func):
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        return ret * 2

    return wrapper


@decorator
def wait_for_deco_a(x, y):
    return x + y


@decorator
def wait_for_deco_b(x, y, z):
    return x + y + z


print(wait_for_deco_a(1, 2))
print(wait_for_deco_b(1, 2, 3))


# decrator(args)返回的是最终需要的装饰器就好了。所以，带参数的装饰器就需要写成下面这样：
def decorator(name):
    print("在这里使用装饰器的name参数：", name)

    def wrapper(func):
        print("在这里也可用装饰器的name参数：", name)

        def _wrapper(*args, **kwargs):
            print("这里还可使用装饰器的name参数：", name)
            ret = func(*args, **kwargs)  # 这里进行原函数的计算
            return ret * 2

        return _wrapper  # 返回可调用对象，_wrapper可以接受原函数的参数

    return wrapper  # 返回真正的装饰器，接受原函数作为第一个参数


@decorator('haha')
def wait_for_deco(x, y):
    return x + y


print(wait_for_deco(2, 6))
