import psutil

#  http://www.jianshu.com/p/a0f7bc1a729d
# cpu 数量
cpu_count = psutil.cpu_count()
# cpu使用率  interval指定的是计算cpu使用率的时间间隔，percpu则指定是选择总的使用率还是每个cpu的使用率
cpu_percent = psutil.cpu_percent(interval=1, percpu=True)

# 内存信息
detail_memory = psutil.virtual_memory()
# svmem(total=17027588096, available=9367650304, percent=45.0, used=7659937792, free=9367650304)
memory_free = psutil.virtual_memory().free / (1024.0 * 1024.0)

# 剩余磁盘 "/"是当前磁盘，可换成其他路径
detail_disk = psutil.disk_usage("/")
# sdiskusage(total=417206063104, used=333170343936, free=84035719168, percent=79.9)
disk_used = str(psutil.disk_usage("/")[2] / (1024.0 * 1024 * 1024))

all_pid = psutil.pids()
# print(all_pid)
for i in all_pid:
    p = psutil.Process(i)
    print(p.name())
    if p.name() == 'python.exe':
        print(p.name())  # 进程名
        print(p.exe())  # 进程的bin路径
        print(p.cwd())  # 进程的工作目录绝对路径
        print(p.create_time())  # 进程创建时间
        print(p.memory_percent())  # 进程内存利用率
        print(p.cpu_times())  # 进程的cpu时间信息,包括user,system两个cpu信息
        print(p.memory_percent())  # 进程内存利用率
        print(p.memory_info())  # 进程内存rss,vms信息
        print(p.num_threads())  # 进程开启的线程数
        break


    def get_info(pid):
        p = psutil.Process(pid)
        print(p.name())  # 进程名
        print(p.exe())  # 进程的bin路径
        print(p.cwd())  # 进程的工作目录绝对路径
        print(p.create_time())  # 进程创建时间
        print(p.memory_percent())  # 进程内存利用率
        print(p.cpu_times())  # 进程的cpu时间信息,包括user,system两个cpu信息
        print(p.memory_percent())  # 进程内存利用率
        print(p.memory_info())  # 进程内存rss,vms信息
        print(p.num_threads())  # 进程开启的线程数

# pid = 14768
# p = psutil.Process(pid)
# print(p.name())   #进程名
# print(p.exe())    #进程的bin路径
# print(p.cwd())    #进程的工作目录绝对路径
# print(p.status() )  #进程状态
# print(p.create_time())  #进程创建时间
# # print(p.uids())   #进程uid信息
# # print(p.gids())    #进程的gid信息
# print(p.cpu_times())   #进程的cpu时间信息,包括user,system两个cpu信息
# print(p.memory_percent())  #进程内存利用率
# print(p.memory_info())    #进程内存rss,vms信息
# print(p.num_threads())  #进程开启的线程数
