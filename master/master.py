import init
from threading import Thread
import os,sys
from socket import *
import select
import task_split
import conf

BUFSIZE = 1024
PORT = 22365

class Demon(Thread):
    def __init__(self,server):
        Thread.__init__(self)
        self.tcpCliSock = socket(AF_INET,SOCK_STREAM)
        self.server = server
    def run(self):
        ADDR = (self.server,PORT)
        print ADDR
        self.tcpCliSock.connect(ADDR)
        rlist = []
        wlist = []
        xlist = []
        rlist.append(self.tcpCliSock)
        while True:
            rl,wl,el = select.select(rlist,wlist,xlist)
            for s in rl:
                data = s.recv(BUFSIZE)
                print data
                if(data=='finished'):
                    print self.server+' finished'
                    return
def send_data(conf_path):
    task_split.task_split(conf_path)
                
if __name__=='__main__':
    #ips = readConf()
    conf_path = '../conf/conf.txt'
    conf.init(conf_path)
    send_data(conf_path)
    #exit()
    config = conf.readConf(conf_path)
    ips = config['ips']
    ths = []
    for ip in ips:
        ths.append(Demon(ip))
    for t in ths:
        t.start()
    for t in ths:
        t.join()
    print 'Demon Stopped'
                
                
            
            
