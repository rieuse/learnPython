# -*- coding: utf-8 -*-
BOT_NAME = 'ScrapyDoutu'

SPIDER_MODULES = ['ScrapyDoutu.spiders']
NEWSPIDER_MODULE = 'ScrapyDoutu.spiders'

# 下面设置随机User Agent
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'ScrapyDoutu.middlewares.RotateUserAgentMiddleware': 400,
}

ROBOTSTXT_OBEY = False  # 不遵循网站的robots.txt策略
CONCURRENT_REQUESTS = 16  # Scrapy downloader 并发请求(concurrent requests)的最大值
DOWNLOAD_DELAY = 0.2  # 下载同一个网站页面前等待的时间，可以用来限制爬取速度减轻服务器压力。
COOKIES_ENABLED = False  # 关闭cookies
