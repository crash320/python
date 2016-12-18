#### 复习第一节的知识
##### urllib2库从简单到复杂
urllib2模块提供了一些api来获取网络上的资源。
通过urlopen()函数获取远程数据的一个类似文件的句柄
```python
url = http://www.baidu.com
reponse = urllib2.urlopen(url)
#response是一个
```
可以通过info()方法来获取HTTP 服务器的头信息
read()方法获取HTTP服务器额数据信息
```python
import urllib2

response = urllib2.urlopen('http://www.baidu.com/')
print 'RESPONSE:', response
print 'URL     :', response.geturl()

headers = response.info()
print 'DATE    :', headers['date']
print 'HEADERS :'
print '---------'
print headers

data = response.read()
print 'LENGTH  :', len(data)
print 'DATA    :'
print '---------'
print data
```
urlopen() is a convenience function that hides some of the details of how the request is made and handled for you. For more precise(精确的) control, you may want to  use a Request object directly.
```python
import urllib2

request = urllib2.Request('http://localhost:8080/')
request.add_header('User-agent', 'PyMOTW (http://www.doughellmann.com/PyMOTW/)')

response = urllib2.urlopen(request)
data = response.read()
print data
```
使用add_header()函数来设置User-agent值

Posting Form Data

You can set the outgoing(发出的) data on the Request to post it to the server.
```python
import urllib
import urllib2

query_args = { 'q':'query string', 'foo':'bar' }

request = urllib2.Request('http://localhost:8080/')
print 'Request method before data:', request.get_method()

request.add_data(urllib.urlencode(query_args))
print 'Request method after data :', request.get_method()
request.add_header('User-agent', 'PyMOTW (http://www.doughellmann.com/PyMOTW/)')

print
print 'OUTGOING DATA:'
print request.get_data()

print
print 'SERVER RESPONSE:'
print urllib2.urlopen(request).read()
```
>**Note:** Although the method is `add_data()`, its effect is not cumulative. Each call replaces the previous data.


#### 构建一个爬虫的基本步骤
##### 1. 获取网页内容
- <font size=5>从客户端请求</font>:使用Request()函数来构建request handler,这个函数需要三个参数,可以直接作为参数赋值,也可以通过add_data()和add_header()函数添加.作为参数,data(字典类型)和headers(字典类型)需要进行封装,最终获得的html就是网页内容
```python
import urllib2
import urllib
user_data = {'a':'b', 'c':'d'}
data = urllib.urlencode(user_data)
headers = {'User-agent':'wspw'}
request = urllib2.Request(url, data, headers})
```
- <font size=5>收取request请求并生成response handler:</font>使用urlopen()函数或者构建opener来获取request
```python
#1. 直接使用urlopen()函数
response = urllib2.urlopen(request)
html = response.read()
#2. 构建opener
proxy_handler = urllib2.ProxyHandler({})
cookie_handler = ...
opener = urllib2.build_opener(proxy_handler)
response = opener.open(request)
html = response.read()
```
- 处理返回的错误
```python
try:
    response = opener.open(request)

except urllib2.URLError as e:
    if hasattr(e, 'reason'):
        print "we failed reach a server"
        print "Error reason:",e.reason
    if hasattr(e, 'code'):
        print "Error code:",e.code
```
##### 2. 分析网页内容(以找到网页链接为例)
在接收到的网页中使用正则表达式匹配找到相关的内容
```python
import re
aref_regx = re.compile('<a[^>] href=["\'](.*?)["\']', re.IGNORECASE)
link_list = re.findall(aref_regx, html)
```
##### 3. 使用urlparse将残缺的网页连接补全,需要base_url和link
```python
import urlparse  #url分析模块
base_url = "http://tieba.baidu.com"
for link in link_list:
    valid_link = urlparse.urljoin(base_url, link)
```
