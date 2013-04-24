import json
import os

def init(conf):
    data = {
	"ips":["118.244.225.90","118.145.12.196"],
        "master_ip":"118.244.224.211",
	"data_file":"/root/data/urls.txt",
	"split_tmp":"/root/split_tmp",
	"master_result":"/root/result",
	"client_result":"/root/result",
        "client_union":"/root/union",
        "client_union_name":"result.txt",
        "task_num":150,
        "process":"../process/test.py",
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
