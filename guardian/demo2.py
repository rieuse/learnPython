import os
import signal
import subprocess
import psutil

pwd = os.getcwd()
all_pid = psutil.pids()


def get_info(pid):
    p = psutil.Process(i)
    print(p.name())  # 进程名
    print(p.exe())  # 进程的bin路径
    print(p.cwd())  # 进程的工作目录绝对路径
    print(p.create_time())  # 进程创建时间
    print(p.memory_percent())  # 进程内存利用率
    print(p.cpu_times())  # 进程的cpu时间信息,包括user,system两个cpu信息
    print(p.memory_percent())  # 进程内存利用率
    print(p.memory_info())  # 进程内存rss,vms信息
    print(p.num_threads())  # 进程开启的线程数


if __name__ == '__main__':
    for pid in all_pid:
        p = psutil.Process(pid)
        if p.name() == 'python.exe':
            pid_pwd = p.cwd()
            if pwd == pid_pwd:
                print(pid)
                os.popen('taskkill.exe /pid:' + str(pid) + ' -f')
                #             print(psutil.virtual_memory().percent)
                #             psutil.pid_exists(pid)
