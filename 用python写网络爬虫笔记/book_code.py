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
import urllib2
import re
#该函数可以捕获异常、重试下载并设置用户代理
def download(url, user_agent='wswp', num_retries=2):
    #num_retries为设定重试的次数
    print 'Downloading:', url
    headers = {'User-agent':user_agent}
    request = urllib2.Request(url, headers=headers)
    try:
        html = urllib2.urlopen(request).read()
    except urllib2.URLError as e:
        print 'Download error:', e.reason
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # 循环重试
                return download(url, user_agent, num_retries-1)
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
def link_crawler(seed_url, link_regex):
    """
    Crawl form the given seed URL following links
    matched by link_regex
    """
    crawl_queue = [seed_url]
    #创建一个网页地址集合
    seen = set(crawl_queue)
    while crawl_queue:
        url = crawl_queue.pop()
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
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    # list of all links from the webpage
    return webpage_regex.findall(html)
link_queue = link_crawler('http://example.webscraping.com',\
    re.compile('/(index|view)/'))
for link in link_queue:
        print link
import sys
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
