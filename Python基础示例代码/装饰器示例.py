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
