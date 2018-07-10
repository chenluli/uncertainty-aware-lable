#! /usr/bin/python
# -*- coding:utf-8 -*-

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import torndb
import json
import os
import decimal
import numpy as np

timesplitfile=np.array([
	["nfday41",1364802616,1364860816],
	["nfday42",1364860817,1364947216],
	["nfday43",1364947217,1365033616],
	["nfday44",1365034324,1365120016],
	["nfday45",1365120024,1365206416],
	["nfday46",1365206417,1365292816],
	["nfday47",1365292817,1365379216]
])

db = torndb.Connection('127.0.0.1', 'vc13', user = 'root', password = 'root')


def connect2json(features,times,connection,wincnt):
    nodes=[]
    links=[]
    for i in range(len(connection)):
        nodes.append({"id":i,"wincnt":wincnt[i],"feature":features[i].tolist(),"lasttime":times[i]})
    for i in range(len(connection)):
        for j in range(i,len(connection)):
            if(connection[i][j]>0):
                links.append({"source":i,"target":j,"cnt":connection[i][j]})
    return nodes,links


begin = 1364947217
end = 1364947397
sql=""
for i in range(len(timesplitfile)):
    if(begin>=int(timesplitfile[i][1]) and begin<=int(timesplitfile[i][2])):
        beginfile=timesplitfile[i][0]
        break
for i in range(len(timesplitfile)):
    if(end>=int(timesplitfile[i][1]) and end<=int(timesplitfile[i][2])):
        endfile=timesplitfile[i][0]
        break
if beginfile==endfile:
    sql = "SELECT count(*) as cnt,sum(firstSeenSrcTotalBytes) as srcbytes,sum(firstSeenDestTotalBytes) as dstbytes,firstSeenSrcIP as srcip,firstSeenDestIP as dstip FROM " + beginfile + " where TimeSeconds >= %s and TimeSeconds < %s group by firstSeenSrcIP,firstSeenDestIP"
else:
    sql = "SELECT count(*) as cnt,sum(firstSeenSrcTotalBytes) as srcbytes,sum(firstSeenDestTotalBytes) as dstbytes,firstSeenSrcIP as srcip,firstSeenDestIP as dstip FROM " + beginfile + " where TimeSeconds >= %s group by firstSeenSrcIP,firstSeenDestIP" + \
          " union SELECT count(*) as cnt,sum(firstSeenSrcTotalBytes) as srcbytes,sum(firstSeenDestTotalBytes) as dstbytes,firstSeenSrcIP as srcip,firstSeenDestIP as dstip FROM " + endfile + " where TimeSeconds < %s group by firstSeenSrcIP,firstSeenDestIP"
print(sql)
data = db.query(sql, begin, end)
nodes=[]
nodesbytes=[]
links=[]

for i in range(len(data)):
    if(data[i]["srcip"] in nodes):
        tmpsrcind=nodes.index(data[i]["srcip"])
        nodesbytes[tmpsrcind]["src"]=nodesbytes[tmpsrcind]["src"]+int(data[i]["srcbytes"])
    else:
        nodes.append(data[i]["srcip"])
        tmpsrcind=len(nodes)-1
        nodesbytes.append({"ip":int(data[i]["srcip"]),"id":tmpsrcind,"src":int(data[i]["srcbytes"]),"dst":0})
    if (data[i]["dstip"] in nodes):
        tmpdstind = nodes.index(data[i]["dstip"])
        nodesbytes[tmpdstind]["dst"] = nodesbytes[tmpdstind]["dst"] + int(data[i]["dstbytes"])
    else:
        nodes.append(data[i]["dstip"])
        tmpdstind = len(nodes) - 1
        nodesbytes.append({"ip":int(data[i]["dstip"]),"id": tmpdstind, "src": 0, "dst": int(data[i]["dstbytes"])})
    links.append({"source": tmpsrcind, "target": tmpdstind, "cnt": int(data[i]["cnt"])})
print("lll")