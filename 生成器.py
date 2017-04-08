g = (x * x for x in range(10))
print(g)
print(next(g))
print(next(g))
print(next(g))

print('next one')
for n in g:
    print(n)