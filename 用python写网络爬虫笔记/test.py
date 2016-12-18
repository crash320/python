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

url = "http://tieba.baidu.com/dota2"
base_url = "http://tieba.baidu.com"
data = {'a':'b', 'c':'d'}
data_encode = urllib.urlencode(data)
print data_encode
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36'
headers = {'User-agent':'user_agent'}
request = urllib2.Request(url, data=None, headers=headers)
# 设置proxy
enable_proxy = False
proxy_handler = urllib2.ProxyHandler({"http":"www.some.host:8080"})
null_proxy_handler = urllib2.ProxyHandler({})
if enable_proxy:
    opener = urllib2.build_opener(proxy_handler)
else:
    opener = urllib2.build_opener(null_proxy_handler)

response = opener.open(request)
html = response.read()
# print html
# html_header_info = response.info()
# print html_header_info
# html_url = response.geturl()
# print html_url
href_regx = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
link_list = re.findall(href_regx, html)
i = 0
for link in link_list:
    i += 1
    link, _ = urlparse.urldefrag(link) # remove hash to avoid duplicates
    valid_link = urlparse.urljoin(base_url, link)
    if i % 100:
        print "origin_link:", link
        print "change_link:", valid_link
        print "\n"


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
