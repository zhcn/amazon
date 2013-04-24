import init
import os
import conf

#dirs = ['isbn']

total = 0
num = 0
dup = 0
isbn_hash = {}

def getIsbn(path,isbn_all):
    #isbn_all = open(destpath,'w')
    global total
    global num
    global dup
    global isbn_hash
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
                    #buf=fp+':'+res+'\t'+isbn_hash[res]+'\n'
                    #log.write(buf)
                if(isbn_hash.has_key(res)==False and len(res)):
                    #if(res=='7040118238'):
                    #    print fp
                    isbn_hash[res] = fp
                    isbn_all.write(res+'\n')        
                    total += 1
    
def union(sourcedir,destpath):
    global total
    global num
    global dup
    global isbn_hash
    total = 0
    num = 0
    dup = 0
    isbn_hash = {}
    isbn_all = open(destpath,'w')
    getIsbn(sourcedir,isbn_all)
    print 'remain:\t'+str(total)
    print 'total:\t'+str(num)
    print 'dupliate:\t'+str(dup)
    isbn_all.close()

def merge(ip,sourcedir,destpath,rdest,myid):
    union(sourcedir,destpath)
    cmd = 'scp '+destpath+' '+ip+':'+rdest+'.'+str(myid)
    os.system(cmd)

if __name__=='__main__':
    config = conf.readConf('../conf/conf.txt')
    master_ip = config['master_ip']
    client_result = config['client_result']
    client_union_path = config['client_union']+'/'+config['client_union_name']
    master_result = config['master_result']
    client_id = config['client_id']
    f = open(client_id,'r')
    myid = f.readlines()[0]
    f.close()
    merge(master_ip,client_result,client_union_path,master_result,myid)
    
    
    
