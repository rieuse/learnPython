# 普通的递归调用 会造成栈的内存溢出
# def fact(n):
#     if n==1:
#         return 1
#     return n*fact(n-1)
# print(fact(100))
# 下面是解决递归叼用栈溢出的方法：尾递归
def fact(n):
    return fact_iter(n,1)
def fact_iter(num,product):
    if num == 1:
        return product
    return fact_iter(num - 1,num * product)

print(fact_iter(6,1))