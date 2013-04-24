import urllib
import urllib2
import sys
import re
import httplib, socket
from datetime import datetime, timedelta
import StringIO
import gzip
import time
import random

#tmp = sys.stdout
#sys.stdout = open('isbnlog','w')

class Regrex:
    def __init__(self):
        #self.re_price = re.compile('<span\s+id="actualpricevalue">\s*<b.*?>.*?(\d+\.\d*).*?</b>')#\s*?<b>/s*isbn:/s*</b>/s*(.*?)/s*</li>')
        self.re_isbn_10 = re.compile('<b>\s*isbn-10:\s*</b>\s*(.*?)\s*</li>')
        self.re_isbn_13 = re.compile('<b>\s*isbn-13:\s*</b>\s*(.*?)\s*</li>')
        self.re_asin = re.compile('<b>\s*asin:\s*</b>\s*(.*?)\s*</li>')
        self.txt = ''
        self.isbn_10 = ''
        self.isbn_13 = ''
        self.asin = ''
    def setTxt(self,txt):
        self.txt = txt
        #m1 = self.re_price.search(txt)
        #m2 = self.re_isbn.search(txt)
        m1 = self.re_isbn_10.search(txt)
        m2 = self.re_isbn_13.search(txt)
        m3 = self.re_asin.search(txt)
        if(m1!=None):
            self.isbn_10 = m1.groups(1)[0]
        else:
            self.isbn_10 = ''
        if(m2!=None):
            self.isbn_13 = m2.groups(1)[0]
        else:
            self.isbn_13 = ''
        if(m3!=None):
            self.asin = m3.groups(1)[0]
        else:
            self.asin = ''
        print self.isbn_10+'\t'+self.isbn_13+'\t'+self.asin
        return self.isbn_10,self.isbn_13,self.asin
        
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

if __name__ == "__main__":
    regrex = Regrex()
    #response = urllib2.urlopen('http://www.amazon.com/Bloodbrothers-Novel-Richard-Price/dp/B0036DE4AA/ref=sr_1_2?s=books&ie=UTF8&qid=1365777577&sr=1-2&keywords=bargain+price')
    #res = regrex.setTxt(response.read().lower())
    #print 'isbn_10:'+res[0]+'\t'+'isbn_13:'+res[1]+'\t'+'asin:'+res[2]+'\n'
    myid = int(sys.argv[1])
    task_num = int(sys.argv[2])
    #furls = open('urls/task_urls/urls'+str(myid)+'.txt','r')
    #isbn = open('result/isbn'+str(myid)+'.txt','w')
    source_file = sys.argv[3]
    result_file = sys.argv[4]
    file_prefix = sys.argv[5]
    result_prefix = sys.argv[6]
    furls = open(source_file+'/'+file_prefix+'.txt','r')
    isbn = open(result_file+'/'+result_prefix+'.txt','w')
    #sys.stdout = open('log/isbnlog'+str(myid)+'.txt','w')
    logfile = open('log/isbnlog'+str(myid)+'.txt','w')
    myurls = furls.readlines()
    #length = len(myurls)/task_num
    #start = length*(myid-1)
    #end = start + length
    #if(myid>=task_num):
    #    end = len(myurls)
    #myurls = myurls[start:end]
    #for url in furls.readlines():
    processed = 0
    #total = end - start
    total = len(myurls)
    for url in myurls:
        flag = True
        trys = 0
        while flag:
            try:
                #print url
                response = _fetch(url)
                #print url
                html = response.read()
                html = html.lower()
                #print html
                res = regrex.setTxt(html)
                buf = 'isbn_10:'+res[0]+'\t'+'isbn_13:'+res[1]+'\t'+'asin:'+res[2]+'\n'
                isbn.write(buf)
                processed = processed + 1
                tmp = 'processed '+str(processed)+' '+str(processed*1.0/total)+' %'
                logfile.write(tmp)
                break
            except Exception,e:
                print e
                if(trys>=3):
                    flag = False
                trys += 1
    isbn.close()
    logfile.close()
    print 'Finished'

        
        
        
