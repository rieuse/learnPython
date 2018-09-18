import threading
import time


class HtmlSppier(threading.Thread):
    def __init__(self, url, sem):
        super().__init__()
        self.sem = sem
        self.url = url

    def run(self):
        time.sleep(2)
        print('download html success')
        self.sem.release()

class UrlProducer(threading.Thread):
    def __init__(self,sem):
        super().__init__()
        self.sem = sem


    def run(self):
        for i in range(20):
            self.sem.acquire()
            html_thread = HtmlSppier(f'http://www.qq.com/pn={i}',self.sem)
            html_thread.start()


if __name__ == '__main__':
    sem = threading.Semaphore(3)
    url_produce = UrlProducer(sem)
    url_produce.start()