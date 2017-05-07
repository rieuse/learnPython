# import threading
# def run(number):
#     print(threading.currentThread().getName())
# if __name__ == '__main__':
#     for i in range(10):
#         # 指明具体的方法和方法需要的参数
#         thread = threading.Thread(target=run, args=(i,))
#         # 开始线程
#         thread.start()

import threading

mylock = threading.RLock()
num = 0


class WorkThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.t_name = name

    def run(self):
        global num
        while True:
            mylock.acquire()
            print('\n%s locked, number: %d' % (self.t_name, num))
            if num >= 4:
                mylock.release()
                print('\n%s released, number: %d' % (self.t_name, num))
                break
            num += 1
            print('\n%s released, number: %d' % (self.t_name, num))
            mylock.release()


def test():
    thread1 = WorkThread('A-Worker')
    thread2 = WorkThread('B-Worker')
    thread1.start()
    thread2.start()


if __name__ == '__main__':
    test()
