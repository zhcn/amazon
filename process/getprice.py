import urllib
import urllib2
import httplib, socket
from datetime import datetime, timedelta
import StringIO
import gzip
import time
import sys
import re
import init
import conf

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
    flag = True
    while flag:
        try:
            handler = urllib2.HTTPHandler()
            opener = urllib2.build_opener(handler)
            trys += 1
            response = opener.open(request)
            print '_fetch open'
            if response.headers.get("Content-Encoding") == 'gzip':
                stream = StringIO.StringIO(response.read())
                return gzip.GzipFile(fileobj=stream)
            return response
        except urllib2.HTTPError,e:
            if e.code == 404:
                flag = False#raise NotFound
                print 'page 404'
        except Exception, e:
            #print e
            time.sleep(random.randint(20,60))
            #print str(e)+' '+url 
            if trys >= MAX_TRY:
                flag = False
                print str(e)+' '+url

class Regrex:
    def __init__(self):
        self.re_results = re.compile('<\s*tbody\s*class="result"\s*>([\s\S]*?)<\s*/tbody\s*>')
        self.re_price = re.compile('<\s*span\s*class="price">\s*\$(.*?)</span>')
        self.re_condition = re.compile('<div\s*class="condition">([\s\S]*?)</div>')
        self.re_seller = re.compile('<div\s*class="seller">([\s\S]*?)</div>')
        #self.re_next = re.compile('<a\s*id="olp_page_next"\s*class="nextoff"\s*href="([\s\S]*?)"')
        self.re_next = re.compile('<a([^>]*?)>\s*next')
        self.re_href = re.compile('href="([\s\S]*?)"')
    def getResults(self,html):
        return self.re_results.findall(html)
    def getNext(self,html):
        nextUrl = self.re_next.findall(html)
        if(len(nextUrl)==0):
            return ""
        else:
            nextUrl = self.re_href.findall(nextUrl[0])
            nextUrl[0] = nextUrl[0].replace('amp;','')
            nextUrl[0] = nextUrl[0].replace('startindex','startIndex')
            res = "http://www.amazon.com"+nextUrl[0]
            #print res
            return res
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
        return (price,condition,notAmazon)
    def getPriceList(self,html):
        priceList = []
        results = self.getResults(html)
        for r in results:
            priceList.append(self.parseResult(r))
        return priceList

def readIsbnPriceList(isbn):
    url_new = 'http://www.amazon.com/gp/offer-listing/'+isbn+'/ref=dp_olp_new?ie=UTF8&condition=new'
    url_used = 'http://www.amazon.com/gp/offer-listing/'+isbn+'/ref=dp_olp_new?ie=UTF8&condition=used'
    res = []
    tmp_url = url_new
    regrex = Regrex()
    while(tmp_url!=''):
        #print tmp_url
        response = _fetch(tmp_url)
        html = response.read()
        html = html.lower()
        res = res+regrex.getPriceList(html)
        tmp_url = regrex.getNext(html)
    tmp_url = url_used
    while(tmp_url!=''):
        response = _fetch(tmp_url)
        html = response.read()
        html = html.lower()
        res = res + regrex.getPriceList(html)
        tmp_url = regrex.getNext(html)
    return res


def calPrice(priceList,condition):
    price_list = []
    for p in priceList:
        if(p[2]==False):
            continue
        if(condition=='new'):
            if(p[1]=='new'):
                price_list.append(p[0])
        elif(condition=='likenew'):
            if(p[1]=='new' or p[1]=='like new'):
                price_list.append(p[0])
        elif(condition=='verygood'):
            if(p[1]=='new' or p[1]=='like new' or p[1]=='very good'):
                price_list.append(p[0])
        elif(condition=='good'):
            if(p[1]=='new' or p[1]=='like new' or p[1]=='very good' or p[1]=='good'):
                price_list.append(p[0])
    #print condition
    #print price_list
    if(len(price_list)<4):
        return -1.3
    price_list = sorted(price_list)
##    for p in price_list:
##        print p
    res = 0
    for i in range(0,4):
        res = res + price_list[i]
    res = res/4.0
    return res


def query(queryfile,resfile):
    f = open(queryfile,'r')
    res_fd =open(resfile,'w')
    preIsbn = '-1'
    priceList = []
    for q in f.readlines():
        print q
        q = q.strip()
        oneQuery = q.split('\t')
        #print oneQuery
        isbn = oneQuery[1]
        condition = oneQuery[2]
        if(isbn!=preIsbn):
            preIsbn = isbn
            priceList = readIsbnPriceList(isbn)
        #print calPrice(priceList,condition)
        res = q+'\t'+str(calPrice(priceList,condition))+'\n'
        res_fd.write(res)


if __name__=='__main__':
    myid = sys.argv[1]
    config = conf.readConf('../conf/conf.txt')
    split_tmp = config['split_tmp']
    split_prefix = config['split_prefix']
    client_result = config['client_result']
    queryfile = split_tmp+'/'+split_prefix+str(myid)+'.txt'
    resultfile = client_result+'/'+'res'+str(myid)+'.txt'
    query(queryfile,'res.txt')
