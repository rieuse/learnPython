from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import requests
import time


def download_html(i):
    url = f'https://www.baidu.com/s?ie=UTF-8&wd={i}'
    response = requests.get(url).text
    return response

ids = list(range(100))

# with ThreadPoolExecutor(max_workers=8) as exe:
#     exe.map(download_html,ids)


# 其他接口使用：
from concurrent.futures import ThreadPoolExecutor, as_completed,wait


executor = ThreadPoolExecutor(max_workers=8)

# 通过 submit 提交执行的函数到线程中
task1 = executor.submit(download_html, (1))
task2 = executor.submit(download_html, (3))

# done() 判断 task 是否完成
print(task1.done())
time.sleep(4)
print(task1.done())

# result() 获取 task 的执行结果 阻塞
print(task1.result())

# cancel() 取消任务，如果任务在执行中或者执行完了是不能取消的
# 现在线程池是8 两个任务都会被提交任务去执行，如果 max_workers = 1，执行task2.cancel()就会成功取消
print(task2.cancel())


# as_completed() 获取已经成功的task的返回数据，阻塞
# as_completed实际上是一个生成器，里面有 yield 会把已经完成的 future (task) 返回结果
ids = list(range(10))
all_task = [executor.submit(download_html,(i)) for i in ids]
time.sleep(8)
# 这是异步的，谁完成就处理谁
for future in as_completed(all_task):
    data = future.result()
    print(f'html response {data}')


# 通过 executor 获取已经完成的task
for data in executor.map(download_html,ids):
    print(f'html response {data}')


# wait() 等待task完成
ids = list(range(10))
all_task = [executor.submit(download_html,(i)) for i in ids]

#  wait 的 return_when 可选项
FIRST_COMPLETED = 'FIRST_COMPLETED'
FIRST_EXCEPTION = 'FIRST_EXCEPTION'
ALL_COMPLETED = 'ALL_COMPLETED'
_AS_COMPLETED = '_AS_COMPLETED'

wait(all_task, return_when=ALL_COMPLETED)
