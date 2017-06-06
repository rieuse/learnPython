# 示例一：
def consumer():  # 定义消费者，由于有yeild关键词，此消费者为一个生成器
    print("[Consumer] Init Consumer ......")
    r = "init ok"  # 初始化返回结果，并在启动消费者时，返回给生产者
    while True:
        n = yield r  # 消费者通过yield接收生产者的消息，同时返给其结果
        print("[Consumer] conusme n = %s, r = %s" % (n, r))
        r = "consume %s OK" % n  # 消费者消费结果，下个循环返回给生产者


def produce(c):  # 定义生产者，此时的 c 为一个生成器
    print("[Producer] Init Producer ......")
    r = c.send(None)  # 启动消费者生成器，同时第一次接收返回结果
    print("[Producer] Start Consumer, return %s" % r)
    n = 0
    while n < 5:
        n += 1
        print("[Producer] While, Producing %s ......" % n)
        r = c.send(n)  # 向消费者发送消息并准备接收结果。此时会切换到消费者执行
        print("[Producer] Consumer return: %s" % r)
    c.close()  # 关闭消费者生成器
    print("[Producer] Close Producer ......")


produce(consumer())


# 示例二：
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
