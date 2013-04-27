import json
import os

def init(conf):
    data = {
	"ips":["118.244.224.3"],
    "master_ip":"118.244.224.211",
    "data_dir":"/root/data",
	"data_file":"/root/data/pricequery.txt",
	"split_tmp":"/root/split_tmp",
	"master_result":"/root/result",
	"client_result":"/root/result",
    "client_union":"/root/union",
    "client_union_name":"result.txt",
    "task_num":30,
    "process":"../process/getprice.py",
    "split_prefix":"urls",
    "merge":"../result_merge/union.py",
    "client_id":"/root/clientid.txt"
        }
    res = json.dumps(data)
    f = open(conf,'w')
    f.write(res)

def readConf(conf):
    f = file(conf)
    data = json.load(f)
    #print data
    return data

init('conf.txt')
#data = readConf('conf.txt')
#print data['ips']
