# -*- coding:utf-8 -*-
# import robotparser
# rp = robotparser.RobotFileParser()
# rp.set_url('http://example.webscraping.com/robots.txt')
# rp.read()
# url = 'http://example.webscraping.com'
# user_agent = 'BadCrawler'
# print rp.can_fetch(user_agent, url)
#
# user_agent = 'GoodCrawler'
# print rp.can_fetch(user_agent, url)
import urllib2
import urlparse

import re
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
        print html
        # 使用opener
    # 遇到错误时多连接几次
    except urllib2.URLError as e:
        print 'Download error:', e.reason
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # 循环重试
                print url
                return download(url, user_agent, proxy, num_retries-1)
    return html

# 得到一个网页的所有连接
def get_links(html):
    #return list
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', \
     re.IGNORECASE)
    return webpage_regex.findall(html)
# download('http://www.mzitu.com')
for link in get_links(download('https://tieba.baidu.com/')):
    print link
