# # -*- coding:utf-8 -*-
# # import robotparser
# # rp = robotparser.RobotFileParser()
# # rp.set_url('http://example.webscraping.com/robots.txt')
# # rp.read()
# # url = 'http://example.webscraping.com'
# # user_agent = 'BadCrawler'
# # print rp.can_fetch(user_agent, url)
# #
# # user_agent = 'GoodCrawler'
# # print rp.can_fetch(user_agent, url)
import urllib2
import urlparse
import urllib
import re
import urlparse

# url = "http://tieba.baidu.com/dota2"
# seed_url = "http://tieba.baidu.com"
seed_url = 'http://www.smartisan.com/'
data = {'a':'b', 'c':'d'}
data_encode = urllib.urlencode(data)
print data_encode
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36'
headers = {'User-agent':'user_agent'}
# request = urllib2.Request(url, data=None, headers=headers)
# print request.get_full_url()
# 设置proxy
proxy_handler = urllib2.ProxyHandler({"http":"www.some.host:8080"})
null_proxy_handler = urllib2.ProxyHandler({})
enable_proxy = False
if enable_proxy:
    proxy = proxy_handler
else:
    proxy = null_proxy_handler

# request = urllib2.Request(url)
# # opener = urllib2.build_opener(proxy_handler)
# response = opener.open(request)
# html = response.read()
# print html
#
# import sys
# sys.exit()
# response = opener.open(request)
# html = response.read()
# # print html
# html_header_info = response.info()
# print html_header_info
# html_url = response.geturl()
# print html_url
# href_regx = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
# link_list = re.findall(href_regx, html)
# i = 0
# for link in link_list:
#     i += 1
#     link, _ = urlparse.urldefrag(link) # remove hash to avoid duplicates
#     valid_link = urlparse.urljoin(seed_url, link)
#     if i % 100:
#         print "origin_link:", link
#         print "change_link:", valid_link
#         print "\n"

def download(url, user_agent="test_agent", data=None, proxy=None, num_retries=2):
    headers = {}
    if user_agent:
        headers['User-agent'] = user_agent
    if data:
        data_encode  = urllib.urlencode(data)
    request = urllib2.Request(url, data, headers=headers)
    opener = urllib2.build_opener(proxy)
    try:
        # response = opener.open(request)
        response = opener.open(request)
        html = response.read()
        # print "ok"
    except urllib2.URLError as e:
        html = '' #为了防止出错而设置的,为了后面的变量可以顺利返回
        if hasattr(e, 'reason'):
            print "Error reason:", e.reason
        if hasattr(e, 'code'):
            if num_retries > 0 and (500 <= e.code < 600):
                print "Error code:", e.code
                download(url, user_agent, data, proxy, num_retries-1)
    return html
def get_links(html):
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    return re.findall(webpage_regex, html)

def intack_link(seed_url, link):
    # link, _ = urlparse.urldefrag(link)
    return urlparse.urljoin(seed_url, link)

def crawl_queue(seed_url, max_urls, max_depth = -1, headers = None, user_agent="wswp", \
                proxy = None, num_retries = 3):
    crawl_queue = [seed_url]
    seen = {seed_url:0}
    headers = headers or {}
    num_urls = 0  #设置获取的最大链接数
    if user_agent:
        headers['User-agent'] = user_agent
    if proxy:
        proxy = proxy
    while crawl_queue:
        # depth = seen[seed_url]
        url = crawl_queue.pop()
        html = download(url, user_agent, data=None, proxy=proxy, num_retries=2)
        depth = seen[url]
        # print html
        if depth != max_depth:
            link_list = set(get_links(html))
            i = 0
            for link in link_list:
                i += 1
                # print "origin_link:", link
                link = intack_link(seed_url, link)
                if i % 10 == 0:
                    print "change_link:", link
                    print "\n"
                if link not in seen:
                    seen[link] = depth + 1
                    crawl_queue.append(link)
        num_urls += 1
        if num_urls == max_urls:
            break
if __name__ == '__main__':
    crawl_queue(seed_url, max_urls=-1, max_depth=2, user_agent=user_agent, proxy=proxy, num_retries=2)
# # def download(url, headers, proxy, num_retries = 2, data=None):
# #     print "Downloading:", url
# #     headers = {'User-agent':user_agent}
# #     request = urllib2.Request(url, headers=headers)
# #     opener = urllib2.build_opener()
# #
# #     if proxy:
# #
# # # 得到一个网页的所有连接
# # def get_links(html):
# #     #return list
# #     webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', \
# #      re.IGNORECASE)
# #     return webpage_regex.findall(html)
# # # download('http://www.mzitu.com')
# # for link in get_links(download('https://tieba.baidu.com/')):
# #     print link

# import urllib2
# import urllib
# url = "http://tieba.baidu.com/dota2"
# response = urllib2.urlopen(url)
# headers_info = response.info()
# print "Header_Info:", headers_info
# data = response.read()
# # query_args = { 'q':'query string', 'foo':'bar' }
# query_args = { 'q':'query string', 'foo':'bar' }
# encode_args = urllib.urlencode(query_args)
# print "Encode", encode_args

# import urllib
# import urllib2
#
# query_args = { 'q':'query string', 'foo':'bar' }
#
# request = urllib2.Request('http://localhost:8080/')
# print 'Request method before data:', request.get_method()
#
# request.add_data(urllib.urlencode(query_args))
# print 'Request method after data :', request.get_method()
# request.add_header('User-agent', 'PyMOTW (http://www.doughellmann.com/PyMOTW/)')
#
# print
# print 'OUTGOING DATA:'
# print request.get_data()
#
# print
# print 'SERVER RESPONSE:'
# print urllib2.urlopen(request).read()
