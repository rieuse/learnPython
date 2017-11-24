import multiprocessing
import os
import subprocess
import psutil
import time

pwd = os.getcwd()
all_pid = psutil.pids()


def judge_spider():
    for pid in all_pid:
        p = psutil.Process(pid)
        if p.name() == 'python.exe':
            pid_pwd = p.cwd()
            if pwd == pid_pwd:
                print('pid: ' + str(pid))
                memory_percent = psutil.virtual_memory().percent
                pid_memory_percent = p.memory_percent()
                print('memory_percent; ' + str(memory_percent), 'pid_memory_percent: ' + str(pid_memory_percent))
                # if memory_percent > 30 and pid_memory_percent > 0.17:
                #     kill_python(pid)
                #     kill_mongo()
                #     time.sleep(5)
                #     print('restart')
                #     start_mongo()
                #     start_spider()
                #     judge_spider()


def start_spider():
    os.system('python spider.py')
    print(os.getpid())


def start_mongo():
    os.system('mongod --dbpath=F:\data\db')
    print('成功开启 mongodb')


def kill_python(pid):
    os.popen('taskkill.exe /pid:' + str(pid) + ' -f')


def kill_mongo():
    for pid in all_pid:
        p = psutil.Process(pid)
        if p.name() == 'mongod.exe':
            os.popen('taskkill.exe /pid:' + str(pid) + ' -f')


if __name__ == '__main__':
    os.system('mongod --dbpath=F:\data\db')
    # p1 = multiprocessing.Process(target=start_mongo, args=())
    # p1.start()
    # time.sleep(3)
    print('成功开启 mongodb')
    # p2 = multiprocessing.Process(target=start_spider, args=())
    # p2.start()
    os.system('python spider.py')
    print(os.getpid())
    # print(p2.pid)
    for pid in all_pid:
        p = psutil.Process(pid)
        if p.name() == 'python.exe':
            print(p.name())
            # judge_spider()
