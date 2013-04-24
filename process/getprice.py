import urllib
import urllib2
import httplib, socket
from datetime import datetime, timedelta
import StringIO
import gzip
import time
import sys
import re

TIMEOUT = 15 #: timeout in seconds
MAX_TRY = 3

HEADERS = [
            ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"),
            ("Accept-language", "en-us,en;q=0.5"),
            ("User-agent", "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2) Gecko/20100207 Namoroka/3.6"),
            ("Accept-encoding","gzip,deflate"),
            ("Accept-charset", "utf-8;q=0.7,*;q=0.7"),
            ("Keep-alive", "115"),
            ("Connection", "keep-alive")
            ]

socket.setdefaulttimeout(TIMEOUT)

def _fetch(url):
    """
    Calls http requests
    """
    request = urllib2.Request(url)
    for k,v in HEADERS:
        request.add_header(k, v)
    trys = 0
    while True:
        try:
            handler = urllib2.HTTPHandler()
            opener = urllib2.build_opener(handler)
            trys += 1
            response = opener.open(request)
            if response.headers.get("Content-Encoding") == 'gzip':
                stream = StringIO.StringIO(response.read())
                return gzip.GzipFile(fileobj=stream)
            return response
        except urllib2.HTTPError,e:
            if e.code == 404:
                raise NotFound
        except Exception, e:
            print e
            if trys >= MAX_TRY:
                raise NetError
            continue


class Regrex:
    def __init__(self):
        self.re_results = re.compile('<\s*tbody\s*class="result"\s*>([\s\S]*?)<\s*/tbody\s*>')
        self.re_price = re.compile('<\s*span\s*class="price">\s*\$(.*?)</span>')
        self.re_condition = re.compile('<div\s*class="condition">([\s\S]*?)</div>')
        self.re_seller = re.compile('<div\s*class="seller">([\s\S]*?)</div>')
    def getResults(self,html):
        return self.re_results.findall(html)
    def parseResult(self,result):
        price = self.re_price.findall(result)
        price = float(price[0])
        #print price
        condition = self.re_condition.findall(result)
        if(condition[0].find('new')!=-1):
            if(condition[0].find('like')!=-1):
                condition = 'like new'
            else:
                condition = 'new'
        elif(condition[0].find('good')!=-1):
            if(condition[0].find('very')!=-1):
                condition = 'very good'
            else:
                condition = 'good'
        else:
            condition = 'others'
        #print condition
        seller = self.re_seller.findall(result)
        notAmazon = True
        #print seller
        if(len(seller)==0):
            notAmazon = False
        #print notAmazon
        print (price,condition,notAmazon)


if __name__=='__main__':
    regrex = Regrex()
    response = _fetch('http://www.amazon.com/gp/offer-listing/B005M4MTY4/sr=/qid=/ref=olp_tab_all?ie=UTF8&colid=&coliid=&me=&qid=&seller=&sr=')
    html = response.read()
    html = html.lower()
    #print html
    results = regrex.getResults(html)
    for result in results:
        regrex.parseResult(result)
