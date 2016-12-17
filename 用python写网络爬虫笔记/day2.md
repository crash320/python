#### 用python写爬虫 day2
上一节内容
>##### 爬虫细节
>1. 相对链接:只有网页的路径部分，而没有协议和服务器部分，可以使用urlparse将其转化为绝对链接
>2. 链接之间存在重复，为了避免重复爬去相同的链接，需要记录哪些链接已经被爬取过。
>3. 解析robots.txt，避免下载禁止爬取的URL
---
解析robots.txt文件，避免下载禁止爬取的URL。使用自带的robotparser模块。

代码样例:
```python
# -*- coding:utf-8 -*-
import robotparser
rp = robotparser.RobotFileParser()
rp.set_url('http://example.webscraping.com/robots.txt')
rp.read()
url = 'http://example.webscraping.com'
user_agent = 'BadCrawler'
print rp.can_fetch(user_agent, url)

user_agent = 'GoodCrawler'
print rp.can_fetch(user_agent, url)

```
其中，can_fetch()函数确定指定的用户代理是否允许访问网页。
可以访问，则返回True，不能返回False。
5. 支持代理
有些网站需要代理才能访问，比如Netflix屏蔽了美国以外的大多数国家。
[request模块可以更友好的实现代理](http://docs.python-requests.org/)
下面是使用urllib2实现的代码
```python
proxy = ...
opener = urllib2.build_opener()
proxy_params = {urlparse.urlparse(url).scheme:proxy}
opener.add_handler(urllib2.ProxyHandler(proxy_params))
response = opener.open(request)
```
6. 下载限速
如果爬取网站的速度过快的话，就会面临被封禁的风险。
所有我们需要在两次下载之间添加延迟，从而对爬虫限速。
实现代码
```python
#下载限速模块
import datetime
import urlparse
import time
class Throttle:
    """在相同网站的两次下载之间设置延迟
    """
    def __init__(self, delay):
        # 延迟时间
        self.delay = delay
        #最后访问网站的时间戳
        self.domains = {}

    def wait(self, url):
        domain = urlparse.urlparse(url).netloc
        last_accessed = self.domains.get(domain)

        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.datetime.now() - \
            last_accessed).seconds
            if sleep_secs > 0:
                #刚才已经访问了该域名，需要等待一会儿
                time.sleep(sleep_secs)
        #更新最后访问的时间
        self.domains[domain] = datetime.datetime.now()
```
Throttle类记录了每个域名上次访问的时间，如果当前时间距离上次访问时间小于指定延迟，则执行睡眠操作。
使用
```
throttle = Throttle(delay)
...
throttle.wait(url)
result = download(url, headers, proxy=proxy,
    num_retries=num_retries)
```
7. 避免爬虫陷阱
&emsp;&emsp;一些网站会动态生成网页内容，这样就会出现无限多的网页。
&emsp;&emsp;避免陷入爬虫陷阱的简单方法是记录到达当前网页经过了多少个链接
也就是深度。当到达最大深度时，爬虫就不再想队列中添加该网页中的链接了。要实现这一功能，我们需要修改seen变量。该变量原先只记录访问过的网页链接，现在修改为一个字典，增加了页面深度的记录。
代码:
```python
def link_crawler(..., max_depth=2):
    max_depth = 2
    seen = {}
    ...
    depth = seen[url]
    if depth != max_depth:
        for link in links:
            if link not in seen:
                seen[link] = depth + 1
                crawl_queue.append(link)
```

8. 最终版本
[完整代码](http://bitbucket.org/wswp/code/src/tip/chapter01/link_crawler3.py)
