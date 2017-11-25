import os
import psutil
import time
import sys

def start_spider():
    os.popen('python spider.py')
    print('start spider succeed')


def start_mongo():
    os.popen('mongod --dbpath=F:\data\db')
    print('start mongod succeed')


def kill_spider(pid):
    os.popen('taskkill /pid {} /f'.format(str(pid)))
    print('kill python over')


def kill_mongo():
    pid = os.popen("tasklist | grep mongod | awk '{print $2}'").read()[:-1]
    print(pid)
    if pid:
        os.popen('taskkill /pid {} /f'.format(pid))
        print('kill mongo over')
    else:
        print('no mongo')


def start_mongo_spider():
    os.popen('mongod --dbpath=f:\data\db')
    os.popen('python spider.py')


def judge_spider(spider_pid):
    p = psutil.Process(spider_pid)
    memory_percent = psutil.virtual_memory().percent
    pid_memory_percent = p.memory_percent()
    print('memory_percent: ' + str(memory_percent), 'pid_memory_percent: ' + str(pid_memory_percent))
    if memory_percent > int(default_memory_percent):
        kill_spider(spider_pid)
        kill_mongo()
        print('restart spider and mongo')
        time.sleep(10)
        main()
    else:
        time.sleep(180)
        main()


def main():
    start_mongo()
    start_spider()
    guardian_pwd = str(os.getpid())
    pids = os.popen("tasklist | grep python | awk '{print $2}'").read()
    pids = pids.split('\n')[:-1]
    if guardian_pwd in pids:
        pids.remove(guardian_pwd)
    if not pids:
        print('no pid, please start spider process')
        return
    spider_pid = pids[0]
    print(spider_pid)
    time.sleep(180)
    judge_spider(int(spider_pid))


if __name__ == '__main__':
    default_memory_percent = sys.argv[1]
    main()
