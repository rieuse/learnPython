from threading import Thread, Condition


class T1(Thread):
    def __init__(self, con):
        super().__init__()
        self.con = con

    def run(self):
        with self.con:
            print(1)
            self.con.notify()
            self.con.wait()
            print(3)
            self.con.notify()
            self.con.wait()


class T2(Thread):
    def __init__(self, con):
        super().__init__()
        self.con = con

    def run(self):
        with self.con:
            self.con.wait()
            print(2)
            self.con.notify()
            self.con.wait()
            print(4)
            self.con.notify()




if __name__ == '__main__':
    con = Condition()
    thread1 = T1(con)
    thread2 = T2(con)

    thread2.start()
    thread1.start()
