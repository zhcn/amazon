import init
import sys
import os
import conf
if __name__=='__main__':
    myid = sys.argv[1]
    config = conf.readConf('../conf/conf.txt')
    split_tmp = config['split_tmp']
    client_result = config['client_result']
    os.system('cp '+split_tmp+'/* '+client_result+'/')
    
