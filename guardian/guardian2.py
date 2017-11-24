# encoding=utf-8
import psutil
import time
import sys

"""
这个脚本用于监控某个进程的CPU和内存使用情况，将信息记录到文件中
"""

if __name__ == '__main__':
    """参数1:进程PID  参数2:保存的文件名(可选) 参数3:时间间隔(可选)  
    """
    # pid = sys.argv[1]
    pid = '4140'
    file_name = sys.argv[2] if len(sys.argv) > 2 else 'Test.txt'
    interval = float(sys.argv[3]) if len(sys.argv) > 3 else 1800
    p = psutil.Process(int(pid))
    ss = 'time: %s\tcpu percent: %f\tmemory usage:%d\n' % (
        time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
        p.cpu_percent(interval=1.0),
        p.memory_info()[0])
    print(ss)
    # try:
    #     while True:
    #         with open(file_name, 'a') as f:
    #             f.write('time: %s\tcpu percent: %f\tmemory usage:%d\n' % (
    #             time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
    #             p.get_cpu_percent(interval=1.0),
    #             p.get_memory_info()[0]))
    #             # 每一段时间记录一次进程的CPU和内存使用信息
    #             time.sleep(interval)
    # except KeyboardInterrupt:
    #     # 中断退出
    #     print('Exit!')
