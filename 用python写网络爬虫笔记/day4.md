##### 3. 使用urlparse将残缺的网页连接补全,需要base_url和link
```python
import urlparse  #url分析模块
base_url = "http://tieba.baidu.com"
for link in link_list:
    valid_link = urlparse.urljoin(base_url, link)
```
-------------
##### 4. 设定网页爬去的深度,以防陷入爬虫陷阱
对于每一个url设定相应的深度depth
当超过这个深度之后,不再对这个链接进行爬取,转向另外一个url
设定
```python
seen = {url:0}
depth = seen[url]
if depth < max_depth:
    ...-->link
    if link not in seen:
        seen[link] = depth + 1
```
---
2016/12/19 16:32:41
#### 第二章:数据抓取
##### 三种抓取网页抓取的方法
1. 正则表达式方式
使用正则表达式需要re包
```python
import re
# 1. 生成pattern
regex = re.compile('...') #其中是正则的一些模式
# 2. 使用findall()函数找出来
find_list = re.findall(regex, html) #html表示得到的网页内容
```
2. Beautiful Soup
使用Beautiful Soup的第一步是将已下载的HTML内容解析为soup文档。
但是由于大多数网页都不具有良好的HTML格式，因此Beautiful Soup需要对其实际格式进行确定。
对于一个确实的网页
```html
<ul class=country>
    <li>Area
    <li>Population
</ul>
```
使用Beautiful Soup可以对其进行调整
```python
from bs4 import BeautifulSoup
broken_html = '<ul class=country><li>Area<li>Population</ul>'
# parse the HTML
soup = BeautifulSoup(broken_html, 'html.parser')
fixed_html = soup.prettify()
print fixed_html
```
输出结果为:
```html
<ul class="country">
 <li>
  Area
  <li>
   Population
  </li>
 </li>
</ul>
```
从上述的执行结果可以看出，Beautiful Soup能够正确解析缺失的引号并闭合标签。
在Beautiful Soup中，可以使用find()和find_all()方法来定位需要的元素。
```python
import re
import urllib2
import urllib
import urlparse
#----------------
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36'
headers = {'User-agent': 'user_agent'}
#-----------------------
def download(url, headers, proxy=None, num_retries=2, data=None):
    print 'Downloading:', url
    request = urllib2.Request(url, data, headers)
    opener = urllib2.build_opener()
    if proxy:
        proxy_params = {urlparse.urlparse(url).scheme: proxy}
        opener.add_handler(urllib2.ProxyHandler(proxy_params))
    try:
        response = opener.open(request)
        html = response.read()
        code = response.code
    except urllib2.URLError as e:
        print 'Download error:', e.reason
        html = ''
        if hasattr(e, 'code'):
            code = e.code
            if num_retries > 0 and 500 <= code < 600:
                # retry 5XX HTTP errors
                return download(url, headers, proxy, num_retries - 1, data)
        else:
            code = None
    return html
#-------------------------------------
from bs4 import BeautifulSoup
url = 'http://example.webscraping.com/places/view/United-Kingdom-239'
html = download(url, headers)
soup = BeautifulSoup(html, 'lxml')
# locate the area row
tr = soup.find(attrs={'id': 'places_area__row'})
print "tr:", tr
td = tr.find(attrs={'class': 'w2p_fw'})  # locate the area tag
print "td:", td
area = td.text
print area
```
3. Lxml
Lxml是基于libxml2这一XML解析库的python封装。该模块使用C语言编写，
解析速度比Beautiful Soup快，不过安装过程也更为复杂。最新的安装说明可以参考
[http://Lxml.de/installation.html](http://Lxml.de/installation.html)
和Beautiful Soup一样，lxml也可以将不合法的HTML解析为同一格式。下面是一个例子
```python
import lxml.html
broken_html = '<ul class=country><li>Area<li>Population</ul>'
tree = lxml.html.fromstring(broken_html) #parse the HTML
fixed_html = lxml.html.tostring(tree, pretty_print=True)
print fixed_html
```
解析王输入内容之后，进入选择元素的步骤，lxml有几种不同的方式，这里选择CSS选择器
因为它更简洁，并且能够在第5章解析动态内容时得以复用。
下面是使用CSS选择器抽取面积数据的实例代码
```python
tree = lxml.html.fromstring(html)
td = tree.cssselect('tr#places_area__row > td.w2p_fw')[0] #关键代码
area = td.text_content()
print area
```
关键代码会找到ID为places_area__row的表格行元素，然后选择class为w2p_fw的表格数据子标签
cssselect需要使用pip单独安装这个模块
CSS选择器
css选择器表示选择元素所使用的模式。下面是一些常用的选择器示例。
```python
选择所有标签 ：*
选择<a>标 签：a
选择所有class = "link"的元素：.link
选择class = "link"的 <a>标签： a.link
选择 id = " home ” 的 <a>标 签： a Jfhome
选择父元素为<a>标签的所有<span>子标 签： a > span
选择<a>标签内部的所有<span>标签：a span
选择title属性为"Home"的所有<a>标签：a[title=Home]
```
W3C已提出CSS3规范，其网址为http://www.w3.org/TR/2011/REC-css3-selectors3-20110929
