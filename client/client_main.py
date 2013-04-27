from threading import Thread
import os,sys
import init
import task_split
import conf

class MyThread(Thread):
    def __init__(self,tid,process,task_num):
        Thread.__init__(self)
        self.tid = tid
        self.task_num = task_num
    def run(self):
        try:
            #os.system('python getIsbn.py '+str(self.tid)+' '+str(self.task_num))
            os.system('python '+process+' '+str(self.tid)+' '+str(self.task_num))
        except Exception,e:
            print e
            
if __name__=='__main__':
    ths = []
    conf_file = '../conf/conf.txt'
    conf.init(conf_file)
    config = conf.readConf(conf_file)
    task_num = config['task_num']
    #os.system('python ./urls/split.py '+str(task_num))
    data_file = config['data_file']
    data_dir = config['data_dir']
    destdir = config['split_tmp']
    split_tmp = destdir
    process = config['process']
    merge = config['merge']
    client_result = config['client_result']
    client_union = config['client_union']
    os.system('rm -rf '+split_tmp)
    os.system('rm -rf '+client_result)
    os.system('rm -rf '+client_union)
    os.system('mkdir '+split_tmp)
    os.system('mkdir '+client_result)
    os.system('mkdir '+client_union)
    task_split.my_task_split(conf_file)
    for i in range(1,task_num+1):
        ths.append(MyThread(i,process,task_num))

    for t in ths:
        t.start()

    for t in ths:
        t.join()
    print 'merge'    
    os.system('python '+merge)
    print 'client main finished'
