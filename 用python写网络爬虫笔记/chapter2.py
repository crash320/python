# -*- coding:utf-8 -*-
import re
import urllib2
import urllib
import urlparse

# url = 'http://example.webscraping.com/view/United-Kingdom-239'
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36'
headers = {'User-agent': 'user_agent'}
# # proxy_handler = urllib2.ProxyHandler({"http": "www.some.host:8080"})
# # null_proxy_handler = urllib2.ProxyHandler({})
# # enable_proxy = False
# # if enable_proxy:
# #     proxy = proxy_handler
# # else:
# #     proxy = null_proxy_handler


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

# html = download(url, headers)
# # print html
# td_regex = re.findall('<td class="w2p_fw">(.*?)</td>', html)
# print td_regex[1]
#
# -------------------------
# from bs4 import BeautifulSoup
# broken_html = '<ul class=country><li>Area<li>Population</ul>'
# # parse the HTML
# soup = BeautifulSoup(broken_html, 'html.parser')
# fixed_html = soup.prettify()
# print fixed_html
#---------------------

# from bs4 import BeautifulSoup
# url = 'http://example.webscraping.com/places/view/United-Kingdom-239'
# html = download(url, headers)
# soup = BeautifulSoup(html, 'lxml')
# # locate the area row
# tr = soup.find(attrs={'id': 'places_area__row'})
# print "tr:", tr
# td = tr.find(attrs={'class': 'w2p_fw'})  # locate the area tag
# print "td:", td
# area = td.text
# print area

#--------------------------
# import lxml.html
# broken_html = '<ul class=country><li>Area<li>Population</ul>'
# tree = lxml.html.fromstring(broken_html)  # parse the HTML
# fixed_html = lxml.html.tostring(tree, pretty_print=True)
# print fixed_html


#------------------------
# import lxml
# import lxml.html
# import lxml.cssselect
# url = 'http://example.webscraping.com/places/view/United-Kingdom-239'
# html = download(url, headers)
# # print html
# tree = lxml.html.fromstring(html)
# # locate the area row
# td = tree.cssselect('tr#places_area__row > td.w2p_fw')[0]
# area = td.text_content()
# print area

FIELDS = ('area', 'population', 'iso', 'country', 'capital',
          'continent', 'tld', 'currency_code', 'currency_name', 'phone',
          'postal_code_format', 'postal_code_regex', 'languages',
          'neighbours')
import re


def re_scraper(html):
    results = {}
    for field in FIELDS:
        results[field] = re.search(
            '<tr id="places_%s__row">.*?<td class="w2p_fw">(.*?)</td>' % field, html).groups()[0]
    # print results
    return results

from bs4 import BeautifulSoup
def bs_scraper(html):
    results = {}
    soup = BeautifulSoup(html, 'lxml')
    for field in FIELDS:
        results[field] = soup.find('table').find('tr', \
            id='places_%s__row' % field).find('td', class_='w2p_fw').text

    return results

import lxml.html
def lxml_scraper(html):
    results = {}
    tree = lxml.html.fromstring(html)
    for field in FIELDS:
        results[field] = tree.cssselect('table > tr#places_%s__row \
            > td.w2p_fw' % field)[0].text_content()
    return results

import time
NUM_ITERATIONS = 1000  # numbers of times to test each scraper
html = download(
    'http://example.webscraping.com/places/view/United-Kingdom-239', headers)
# print html
for name, scraper in [('Regular expressions', re_scraper),
                      ('BeautifulSoup', bs_scraper),
                      ('Lxml', lxml_scraper)]:
    #     pass
    # record start time of scrape
    # name = "re"
    start = time.time()
    for i in range(NUM_ITERATIONS):
        if scraper == re_scraper:
            re.purge()
        result = scraper(html)
        # print result
        # print html
        # check scraped result is as expected,python中的assert是用来检查一个条件，
        # 如果它为真，就不做任何事。如果它为假，则会抛出AssertError并且包含错误信息
        # print result['area']
        if i == 900:
            print "900:YES!"
        # if result.has_key('area'):
            # print result['area']
        assert(result['area'] == '244,820 square kilometres')
    # record end time of scrape and output the total
    end = time.time()
    print '%s: %.2f seconds' % (name, end - start)
