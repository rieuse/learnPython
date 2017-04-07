# -*- coding: utf-8 -*-
def move(n,a,b,c,):
    if n==1:
        global x
        print(a,'-->',c)
        num= num + 1
    else:
        move(n-1,a,c,b)
        move(1,a,b,c)
        move(n-1,b,a,c)
move(3,'A','B','C')
print(num)

