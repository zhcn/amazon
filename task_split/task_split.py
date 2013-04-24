import os
import conf

def split(task_num,source,destdir,prefix):
    f = open(source,'r')
    split_num = task_num
    lst = []
    for i in range(0,split_num):
        lst.append([])
    count = 0
    urls = f.readlines()
    total = len(urls)
    for r in urls:
        lst[count%split_num].append(r)
        count += 1
    for i in range(0,split_num):
        fn = destdir+'/'+prefix+str(i+1)+'.txt'
        f2 = open(fn,'w')
        for r in lst[i]:
            f2.write(r)
        f2.close()
    print 'split finished'

def sendTask(ips,tdir,prefix,rdest):
    for i in range(1,len(ips)+1):
        cmd = 'scp '+tdir+'/'+prefix+str(i)+'.txt'+' '+ips[i-1]+':'+rdest 
        os.system(cmd)
    print 'tasks send finished'

#split total urls to these clients
def task_split(conf_path):
    config = conf.readConf(conf_path)
    ips = config['ips']
    split_tmp = config['split_tmp']
    data_file = config['data_file']
    task_num = len(ips)
    prefix = config['split_prefix']
    data_source = data_file
    rdest = data_file
    split(task_num,data_source,split_tmp,prefix)
    sendTask(ips,split_tmp,prefix,rdest)

#split one client urls to many smaller ones to each process threads
def my_task_split(conf_path):
    config = conf.readConf(conf_path)
    split_tmp = config['split_tmp']
    data_file = config['data_file']
    task_num = config['task_num']
    prefix = config['split_prefix']
    split(task_num,data_file,split_tmp)
    
    
    
