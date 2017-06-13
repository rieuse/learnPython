import binascii

b = binascii.a2b_hex('e4bda0e5a5bde5958a')
l = b.decode(encoding='utf-8')
print(l)
