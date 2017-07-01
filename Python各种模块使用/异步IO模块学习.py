from lxml import etree
import aiohttp, asyncio
import time

list_url = ["https://www.douban.com/doulist/41691053/?start={}&sort=seq&sub_type=4".format(number) for number in
            range(0, 125, 25)]


async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as html:
            response = await html.text(encoding="utf-8")
            return response


async def parser(url):
    response = await fetch(url)
    dom = etree.HTML(response)
    selector = dom.xpath('//div[starts-with(@id,"item")]')
    for item in selector:
        print(item.xpath('div/div[2]/div[@class="title"]/a/text()')[0].strip(
            "\n").strip())  # div//div表示div后面的class="title"的div不管它在此div下什么位置


# 给一个函数添加了async关键字，就会把它变成一个异步函数
# 每个线程有一个事件循环，主线程调用asyncio.get_event_loop时会创建事件循环
# 把异步的任务丢给这个循环的run_until_complete方法，事件循环会安排协同程序的执行
# async关键字将一个函数声明为协程函数，函数执行时返回一个协程对象。
# await关键字将暂停协程函数的执行，等待异步IO返回结果。

# start = time.time()
loop = asyncio.get_event_loop()
tasks = [parser(url) for url in list_url]
loop.run_until_complete(asyncio.gather(*tasks))
# print(time.time() - start)
