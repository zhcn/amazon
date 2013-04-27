import init
from threading import Thread
import os,sys
from socket import *
import select

HOST = ''
BUFSIZE = 1024
PORT = 22365
ADDR = (HOST,PORT)

class Demon(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.tcpSerSock = socket(AF_INET,SOCK_STREAM)
        print ADDR
        self.tcpSerSock.bind(ADDR)
        self.tcpSerSock.listen(5)
        print gethostbyname(gethostname())
    def task(self,master_addr):
        os.system('python client_main.py')
    def run(self):
        localIP = gethostbyname(gethostname())
        rlist = []
        wlist = []
        xlist = []
        rlist.append(self.tcpSerSock)
        while True:
            rl,wl,el=select.select(rlist,wlist,xlist)
            for s in rl:
                connection,master_addr= s.accept()
                connection.send(localIP+' started')
                self.task(master_addr)
                connection.send('finished')

if __name__=='__main__':
    os.system('rm -rf /root/data')
    os.system('mkdir /root/data')
    damon = Demon()
    damon.start()
    damon.join()
    print 'Demon Stopped'
                
                
            
            
