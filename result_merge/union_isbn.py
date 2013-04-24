import os
import re

#dirs = ['isbn']

isbn_all = open('isbnAll.txt','w')
asin_all = open('asinAll.txt','w')
log = open('log.txt','w')

total = 0
num = 0
dup = 0

isbn_hash = {}

def getIsbn(path):
    global asin_all
    global isbn_all
    global total
    global isbn_hash
    global num
    global dup
    files = os.listdir(path)
    for f in files:
        fp = path+'/'+f
        #print fp
        if(os.path.isdir(fp)):
            getIsbn(fp)
        else:
            fd = open(fp)
            for r in fd.readlines():
                num += 1
                #pos = r.rfind('\t')
                res = r.strip()
                if(isbn_hash.has_key(res)):
                    dup += 1
                    buf=fp+':'+res+'\t'+isbn_hash[res]+'\n'
                    log.write(buf)
                if(isbn_hash.has_key(res)==False and len(res)):
                    #if(res=='7040118238'):
                    #    print fp
                    isbn_hash[res] = fp
                    isbn_all.write(res+'\n')        
                    total += 1
                    pos = res.find('asin:')
                    tmp = res[pos+len('asin:'):-1]
                    pos2 = res.find('isbn_10:')
                    pos3 = res.find('isbn_13')
                    tmp2 = res[pos2+len('isbn_10:'):pos3]
                    if(tmp.strip()!='' and tmp2.strip()!=''):
                        asin_all.write(res+'\n')
    
#for d in dirs:
#    files = os.listdir(d)
#    for f in files:
#        fd = open(d+'/'+f,'r')
#        for r in fd.readlines():
#            pos = r.rfind('\t')
##            res = r[:pos]
##            if(isbn_hash.has_key(res)==False and len(res)):
##                isbn_hash[res] = 1
##                isbn_all.write(res+'\n')        
##                total += 1
getIsbn('tmp')
print total
print num
print dup
isbn_all.close()
asin_all.close()
log.close()
