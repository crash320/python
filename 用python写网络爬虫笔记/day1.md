##### 主要学习内容
1. 从页面抓取数据
2. 提取缓存中的数据
3. 使用多个线程和进程进行并发抓取
4. 如何抓取动态页面中的内容，
5. 与表单进行交互，处理页面中的验证码问题
6. 用scarpy和portia来进行数据抓取

##### 阅读这本书的前提
1. [源代码](http://bitbucket.org/wswp/code)
2. [示例网站](http://example.webscraping.com),这个网站限制了下载内容的速度
3. [搭建网站示例](http://bitbucket.org/wswp/places)
4. [关于CSS、HTTP、AJAX、WebKit知识的了解](http://www.w3schools.com)

##### 了解网络爬虫
1. [robots.txt文件，一般在网站根目录中](http://baike.baidu.com/link?url=unvxdu-iDNP5pdY7w6L1Z0KaX4H9Sxsk8b5lVF1f9RIu32-DRFoJdqztdJ4MuImimgAtooRWdss8x2PFAUZGGDzvURqmud6prKU1F7lSayqGGFVBTL68NWwoA3DZjMwH5sxaD8EuCWqVLP__somGSK)
2. [Sitemap标准格式](https://www.sitemaps.org/protocol.html)
3. [估算网站大小](http://www.google.com/advanced_search)
4. 识别网站所用技术: 使用builtwith模块，builtwith.parse('website')
5. 寻找网站所有者:使用whois模块
```python
pip install python-whois
whois.whois('appspot.com')
```
6. [HTTP错误的完整列表](https://tools.ietf.org/html/rfc7231#section-6)

##### 爬虫细节
1. 相对链接:只有网页的路径部分，而没有协议和服务器部分，可以使用urlparse将其转化为绝对链接
2. 链接之间存在重复，为了避免重复爬去相同的链接，需要记录哪些链接已经被爬取过。
3. 解析robots.txt，避免下载禁止爬取的URL
