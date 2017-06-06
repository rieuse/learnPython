def consumer():
    r = ''
    while True:
        n = yield r
        if not n:
            return
        print('consuming the event %s' % n)
        r = '200 OK'


def produce(c):
    c.send(None)
    for n in range(1, 6):
        print('producing event %s' % n)
        r = c.send(n)
        print('the consumer response %s' % r)
    c.close()


c = consumer()
produce(c)
