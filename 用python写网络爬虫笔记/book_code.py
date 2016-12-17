# -*- coding:utf-8 -*-
# # print int('42') + 3
# print('Hello,world!')
# print('What is your name?')
# myname = input()
# print('It\'s good to meet you, ' + myname)
# print(len(myname))
# print(10)
# help(round)
# test_num = 23
# print round(test_num, 4)
import sys
import urllib2
import re
#检查robots.txt
import robotparser
rp = robotparser.RobotFileParser()
rp.set_url('http://example.webscraping.com/robots.txt')
rp.read()
#设置全局变了user-agent
user_agent = 'wswp'

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
#该函数可以捕获异常、重试下载并设置用户代理
def download(url, user_agent='wswp',proxy=None, num_retries=2):
    #num_retries为设定重试的次数
    print 'Downloading:', url
    headers = {'User-agent':user_agent}
    request = urllib2.Request(url, headers=headers)

    opener = urllib2.build_opener()
    if proxy:
        proxy_params = {urlparse.urlparse(url).scheme:proxy}
        opener.add_handler(urllib2.ProxyHandler(proxy_params))
    try:
        # html = urllib2.urlopen(request).read()
        html = opener.open(request).read()
        # 使用opener

    except urllib2.URLError as e:
        print 'Download error:', e.reason
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # 循环重试
                return download(url, user_agent, proxy,1)
    return html

def crawl_sitemap(url):
    #download the sitemap file
    sitemap = download(url)
    # extract the sitemap links
    links = re.findall('<loc>(.*?)</loc>', sitemap)
    #download each link
    for link in links:
        html = download(link)
        #scrape html here
import urlparse
#讲相对链接转化为绝对链接
def link_crawler(seed_url, link_regex, max_depth=2):
    """
    Crawl form the given seed URL following links
    matched by link_regex
    """
    #设置最大深度为2
    max_depth = 2
    crawl_queue = [seed_url]
    #创建一个网页地址集合
    # seen = set(crawl_queue)
    seen = {}
    depth = seen[url]
    while crawl_queue:
        url = crawl_queue.pop()
        # 检查url能不能通过robots.txt的限制
        # print user_agent, url
        if not rp.can_fetch('wswp',url):
            print 'Blocked by robots.txt:', url
        else:
            html = download(url)
            # filter for links matching our regular expression
            for link in get_links(html):
                if re.match(link_regex, link):
                    #使用urljoin链接网页路径
                    link = urlparse.urljoin(seed_url, link)
                    #检查是否已经遍历过这个网页
                    if link not in seen:
                        seen.add(link)
                        print link
                        crawl_queue.append(link)

    return crawl_queue
def get_links(html):
    """
    Return a list of links from html
    ----------------
     a regular expression to extract
    all links form the webpage
    """
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']',\
     re.IGNORECASE)
    # list of all links from the webpage
    return webpage_regex.findall(html)

throttle = Throttle(delay)


link_queue = link_crawler('http://example.webscraping.com',\
    re.compile('/(index|view)/'))
for link in link_queue:
        print link

sys.exit()

# 1.遇到错误状态码
# download('http://httpstat.us/500')
# 2.需要设置浏览器代理
# download('http://www.meetup.com/')
# print(download('http://www.baidu.com'))
# 3.依靠sitemap遍历网站
# crawl_sitemap('http://example.webscraping.com/sitemap.xml')
# 4.忽略字符串别名
# download('http://example.webscraping.com/view/1')

# import itertools
# for page in itertools.count(1):
#     url = 'http://example.webscraping.com/view/-%d' % page
#     html = download(url)
#     if html is None:
#         break
#     else:
#         # success - can scrape the result
#         # pass

# maximum number of consecutive download errors allowed
max_errors = 5
# current number of consecutive download errors
num_errors = 0
import itertools

for page in itertools.count(1):
    url = 'http://example.webscraping.com/view/-%d' % page
    html = download(url)
    if html is None:
        # recieved an error trying to download this webpage
        num_errors += 1
        if num_errors == max_errors:
            #reached maximum number of consecutive errors so exit
            break
    else:
        #success - can scrape the result
        # ...
        num_errors = 0
