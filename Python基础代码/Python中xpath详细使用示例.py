from lxml import etree

sample1 = """<html>
  <head>
    <title>My page</title>
  </head>
  <body>
    <h2>Welcome to my <a href="#" src="x">page</a></h2>
    <p>This is the first paragraph.</p>
    <!-- this is the end -->
  </body>
</html>
"""


def getxpath(html):
    return etree.HTML(html)


s1 = getxpath(sample1)
# 获取标题(两种方法都可以，第一种为绝对地址，第二种为相对地址)
s1.xpath('//title/text()')
s1.xpath('/html/head/title/text()')
s1.xpath('//h2/a/@src')
s1.xpath('//@href')
s1.xpath('//text()')
s1.xpath('//comment()')
sample2 = """
<html>
  <body>
    <ul>
      <li>Quote 1</li>
      <li>Quote 2 with <a href="...">link</a></li>
      <li>Quote 3 with <a href="...">another link</a></li>
      <li><h2>Quote 4 title</h2> ...</li>
    </ul>
  </body>
</html>
"""
s2 = getxpath(sample2)
# 所有的li
s2.xpath('//li/text()')
# 获取第1个li
s2.xpath('//li[position() = 1]/text()')
s2.xpath('//li[1]/text()')
# 获取第2个li
s2.xpath('//li[position() = 2]/text()')
s2.xpath('//li[2]/text()')
# 所有基数位的li
s2.xpath('//li[position() mod2 = 1]/text()')
# 所有偶数位的li
s2.xpath('//li[position() mod2 = 0]/text()')
# 取li最后一个的
s2.xpath('//li[last()]/text()')
# li下面有a的
s2.xpath('//li[a]/text()')
# li 下面有a活着h2的
s2.xpath('//li[a or h2]/text()')

# 获取a 和 h2
s2.xpath('//a/text()|//h2/text()')

sample3 = """<html>
  <body>
    <ul>
      <li id="begin"><a href="https://scrapy.org">Scrapy</a>begin</li>
      <li><a href="https://scrapinghub.com">Scrapinghub</a></li>
      <li><a href="https://blog.scrapinghub.com">Scrapinghub Blog</a></li>
      <li id="end"><a href="http://quotes.toscrape.com">Quotes To Scrape</a>end</li>
      <li data-xxxx="end" abc="abc"><a href="http://quotes.toscrape.com">Quotes To Scrape</a>end</li>
    </ul>
  </body>
</html>
"""
s3 = getxpath(sample3)
# 获取 a标签下 href以https开始的
s3.xpath('//a[starts-with(@href, "https")]/text()')
# 获取 href=https://scrapy.org
s3.xpath('//li/a[@href="https://scrapy.org"]/text()')
# 获取 id=begin
s3.xpath('//li[@id="begin"]/text()')
# 获取text=Scrapinghub
s3.xpath('//li/a[text()="Scrapinghub"]/text()')
# 获取某个标签下 某个参数=xx
s3.xpath('//li[@data-xxxx="end"]/text()')
s3.xpath('//li[@abc="abc"]/text()')
sample4 = u"""
<html>
  <head>
    <title>My page</title>
  </head>
  <body>
    <h2>Welcome to my <a href="#" src="x">page</a></h2>
    <p>This is the first paragraph.</p>
    <p class="test">
    编程语言<a href="#">python</a>
    <img src="#" alt="test"/>javascript
    <a href="#"><strong>C#</strong>JAVA</a>
    </p>
    <p class="content-a">a</p>
    <p class="content-b">b</p>
    <p class="content-c">c</p>
    <p class="content-d">d</p>
    <p class="econtent-e">e</p>
    <!-- this is the end -->
  </body>
</html>
"""
s4 = etree.HTML(sample4)
s4.xpath('//p[@class="test"]/text()')
# 获取p下面的所有文字
print(s4.xpath('string(//p[@class="test"])').strip())
# 获取所有class中有content的
s4.xpath('//p[starts-with(@class,"content")]/text()')
s4.xpath(('//*[contains(@class,"content")]/text()'))
