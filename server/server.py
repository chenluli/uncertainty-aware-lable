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
from tornado.options import define, options
from timeline_fun import *
from SDAE import *
from get_feature import *
from soinn import *
import random
from sklearn.manifold import TSNE
from sklearn.manifold import MDS

'''
newtest = np.array([[-0.06685685,  0.05367819, -0.08977896,  2.40567605,  1.58864089, -0.12820046,
   0.2649854,   0.60084742,  0.50951567,  0.07818669,  1.00566211,  0.81230254,
  -0.13127592, -0.41167912,  0.0559229,  -0.13527702, -0.09619706, -0.03217732,
   0.54247754, -0.03064785,  0.130123,   -0.38209966,  4.11532691,  2.0120121,
   4.50189982, -0.17298871,  1.80111208,  0.93372705,  1.64049115, -0.86668314,
   4.08840084,  2.11945393,  4.35943304, -0.20614019,  1.79055654,  0.9352652,
   1.63977831, -0.38306902,  2.0422067,   1.12341889,  1.83718121, -0.22892974,
   1.32974026,  0.97081352,  1.62689211]],dtype=np.float32)
print(newdatafeature(newtest))
'''

define("port", default=8661, help = "run on the given port", type = int)
db = torndb.Connection('127.0.0.1', 'vc13', user = 'root', password = 'root')

# the path to server html, js, css files
client_file_root_path = os.path.join(os.path.split(__file__)[0],'../client')
client_file_root_path = os.path.abspath(client_file_root_path)

saveday=7
starttime=1364774400#1364802616#最早时间
endtime=1365325684#最晚时间 1365379216
inittime=1365078600#1365325500#1365078600#初始化时间 假设之前的数据已经统计好了
nowtime=inittime#模拟实时时 进行到的时间
selectedtime=inittime#时间轴选中的时间
inittype=0#初始化时间轴类型
curtype=inittype#当前时间轴类型



'''
0:TotalBytes all protocal
1:TotalBytes src protocal
2:TotalBytes dst protocal
3:TotalBytes all port
4:TotalBytes src port
5:TotalBytes dst port
'''

timesplitfile=np.array([
	["nfday41",1364802616,1364860799],
	["nfday42",1364860800,1364947199],
	["nfday43",1364947200,1365033599],
	["nfday44",1365033600,1365119999],
	["nfday45",1365120000,1365206399],
	["nfday46",1365206400,1365292799],
	["nfday47",1365292800,1365379199]
])
tlfile=[
    ["nfday41tl",1364802616,1364860799],
	["nfday42tl",1364860800,1364947199],
	["nfday43tl",1364947200,1365033599],
	["nfday44tl",1365033600,1365119999],
	["nfday45tl",1365120000,1365206399],
	["nfday46tl",1365206400,1365292799],
	["nfday47tl",1365292800,1365379199]
]

timelabels=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]

tl_pro=init_file("_pro.csv",inittime,starttime,saveday,tlfile)
tl_port=init_file("_port.csv",inittime,starttime,saveday,tlfile)

curday,curhour,curminu=getcurtimeindex(inittime,starttime)
daycnt=calcu_tl_day(inittype,tl_pro,tl_port)
hourcnt=calcu_tl_hour(curday,inittype,tl_pro,tl_port)
minucnt=calcu_tl_minu(curday,curhour,inittype,tl_pro,tl_port)

newdata_minute=[]

def readfile(filename):
    data = []
    with open("../client/data/"+filename, 'r') as file:
        csvReader = csv.reader(file)
        for line in csvReader:
            data.append(np.array(line, dtype=np.float32))
    data=np.array(data)
    return newdatafeature(data)


print("load features")
exist_feature_origin, exist_feature=init_feature(inittime,starttime)
exist_feature_origin=np.array(exist_feature_origin)

print("initSOINN 1")
soinn_node_1,soinn_connection_1,soinn_wincnt_1,soinn_threshold_1,soinn_age_1=initSOINN(exist_feature, 300, 500, 0.1, False)
print(len(soinn_node_1))
print("initSOINN 2")
soinn_node_2,soinn_connection_2,soinn_wincnt_2,soinn_threshold_2,soinn_age_2=initSOINN(soinn_node_1, 120, 50000, 0.1, False)
print(len(soinn_node_2))
print("initSOINN 3")
timematchnode,soinn_node,soinn_connection,soinn_wincnt,soinn_threshold,soinn_age=matchdata2(exist_feature,soinn_node_2,soinn_connection_2,soinn_wincnt_2,soinn_threshold_2,soinn_age_2, 300)
#timematchnode=np.array(timematchnode)
timematchnode1=np.array(timematchnode)


print("reduce dimension")
soinn_node = np.array(soinn_node)
soinn_node_embedded = TSNE(n_components=2).fit_transform(soinn_node)

print("init distance")
soinn_distance=calcu_dis(soinn_node)
print("init uncertainty")
nodenum=soinn_node.shape[0]
soinn_uncertainty=np.zeros((2,nodenum))#normal,abnormal
print("connect2json")
nodes, links=connect2json(soinn_node_embedded,soinn_connection,soinn_age,soinn_wincnt,soinn_threshold)


queryprecondition=" and firstSeenSrcIP!=2885681153 and firstSeenDestIP!=2885681153 and firstSeenSrcPort!=0 and firstSeenDestPort!=0 and firstSeenDestIP!=4026531834 "



def init_importantips():
    data = []
    with open("../client/data/importantips.csv", 'r') as file:
        csvReader = csv.reader(file)
        for line in csvReader:
            data.append(np.array(line))
            data[len(data)-1][0]=int(data[len(data)-1][0])
            data[len(data)-1][2]=int(data[len(data)-1][2])
    data = np.array(data)
    return data

importantips=init_importantips()


def getTimeRangeData(begin, end):
    for i in range(len(timesplitfile)):
        if(begin>=int(timesplitfile[i][1]) and begin<=int(timesplitfile[i][2])):
            beginfile=timesplitfile[i][0]
            break
    for i in range(len(timesplitfile)):
        if(end>int(timesplitfile[i][1]) and end<=int(timesplitfile[i][2])+1):
            endfile=timesplitfile[i][0]
            break
    if beginfile==endfile:
        sql = "select * from "+beginfile+" where TimeSeconds >= %s and TimeSeconds < %s"+queryprecondition+"order by TimeSeconds"
    else:
        sql = "select * from " + beginfile + " where TimeSeconds >= %s"+queryprecondition+""+\
            " union select * from " + endfile + " where TimeSeconds < %s"+queryprecondition+"order by TimeSeconds"
    #print(sql)
    return db.query(sql, begin, end)


def cntDB2Timeline(begin, end):
    #读取数据库
    #更新newdata_minute
    #插入更新tl_port、tl_pro
    global tl_pro
    global tl_port
    global newdata_minute
    newdata_minute=getTimeRangeData(begin, end)
    portappend,proappend=cntdatabymin(newdata_minute, begin, end)
    #插入新端口数据
    for i in range(len(tl_port)):
        if len(tl_port[i]) < 1440:
            tl_port[i].append(portappend)
            break
    # 插入新协议数据
    for i in range(len(tl_pro)):
        if len(tl_pro[i]) < 1440:
            tl_pro[i].append(proappend)
            break
'''
cntDB2Timeline(selectedtime+60, selectedtime+120)
newfeat=generate_feature(newdata_minute)
print(newfeat)
print("lll")
'''

'''
cntDB2Timeline(selectedtime+60, selectedtime+120)
print(tl_pro[2][750])
print(tl_pro[2][751])
print(tl_port[2][750])
print(tl_port[2][751])
print("lll")
'''


def getipbytes(ipint,iptype,endtime):
    end=endtime+60
    begin=end-60*60
    sql = ""
    for i in range(len(timesplitfile)):
        if (begin >= int(timesplitfile[i][1]) and begin <= int(timesplitfile[i][2])):
            beginfile = timesplitfile[i][0]
            break
    for i in range(len(timesplitfile)):
        if (end > int(timesplitfile[i][1]) and end <= int(timesplitfile[i][2]) + 1):
            endfile = timesplitfile[i][0]
            break
    if beginfile == endfile:
        if(iptype=="src"):
            sql="SELECT TimeSeconds, sum(firstSeenSrcTotalBytes) as srcbytes FROM " + beginfile + " where firstSeenSrcIP="+str(ipint)+" and TimeSeconds>=%s and TimeSeconds<%s"+queryprecondition+"group by TimeSeconds order by TimeSeconds"
        else:
            sql = "SELECT TimeSeconds, sum(firstSeenDestTotalBytes) as dstbytes FROM " + beginfile + " where firstSeenDestIP="+str(ipint)+" and TimeSeconds>=%s and TimeSeconds<%s"+queryprecondition+"group by TimeSeconds order by TimeSeconds"
    else:
        if (iptype == "src"):
            sql = "SELECT TimeSeconds, sum(firstSeenSrcTotalBytes) as srcbytes FROM " + beginfile + " where firstSeenSrcIP="+str(ipint)+" and TimeSeconds >= %s" + queryprecondition + "group by TimeSeconds" + \
                  " union SELECT TimeSeconds, sum(firstSeenSrcTotalBytes) as srcbytes FROM " + endfile + " where firstSeenSrcIP="+str(ipint)+" and TimeSeconds < %s" + queryprecondition + "group by TimeSeconds order by TimeSeconds"
        else:
            sql = "SELECT TimeSeconds, sum(firstSeenDestTotalBytes) as dstbytes FROM " + beginfile + " where firstSeenDestIP=" + str(ipint) + " and TimeSeconds >= %s" + queryprecondition + "group by TimeSeconds" + \
                  " union SELECT TimeSeconds, sum(firstSeenDestTotalBytes) as dstbytes FROM " + endfile + " where firstSeenDestIP=" + str(ipint) + " and TimeSeconds < %s" + queryprecondition + "group by TimeSeconds order by TimeSeconds"
    data = db.query(sql, begin, end)
    print("getipbytes",begin,end)
    datagrouped=[]
    for i in range(60):
        datagrouped.append({"TimeSeconds":begin+i*60,"bytes":0})
    for i in range(len(data)):
        timestamp = int(data[i]["TimeSeconds"])
        bytes = int(data[i][iptype+"bytes"])
        tmpind=int((timestamp-begin)/60)
        datagrouped[tmpind]["bytes"]=datagrouped[tmpind]["bytes"]+bytes
    #print(sql)
    #print(data)
    #return data
    return datagrouped
#getipbytes(2886336515,"src",1364864342)
#getipbytes(2886336515,"src",1364860806)

def getipbytes2(ipint,iptype,endtime):
    ipint=int(ipint)
    end=endtime+60
    begin=end-60*60
    beginfile=0
    endfile=0
    datagrouped = []
    for i in range(len(timesplitfile)):
        if (begin >= int(timesplitfile[i][1]) and begin <= int(timesplitfile[i][2])):
            beginfile = i
            break
    for i in range(len(timesplitfile)):
        if (end > int(timesplitfile[i][1]) and end <= int(timesplitfile[i][2]) + 1):
            endfile = i
            break
    if beginfile == endfile:
        filename = "../client/data/iptraffic"+ iptype+ str(beginfile + 1) + ".csv"
        with open(filename, 'rb') as f:
            for line in f:
                segs = line.split(",")
                tmpip = int(segs[0])
                if(tmpip!=ipint):
                    continue
                else:
                    tmpind = int((begin - beginfile * 24 * 60 * 60 - starttime) / 60)+1
                    for i in range(60):
                        datagrouped.append({"TimeSeconds": begin + i * 60, "bytes": int(segs[tmpind+i])})
                    break
    else:
        filename1 = "../client/data/iptraffic" + iptype + str(beginfile + 1) + ".csv"
        filename2 = "../client/data/iptraffic" + iptype + str(endfile + 1) + ".csv"
        with open(filename1, 'rb') as f:
            for line in f:
                segs = line.split(",")
                tmpip = int(segs[0])
                if(tmpip!=ipint):
                    continue
                else:
                    tmpind = int((begin - beginfile * 24 * 60 * 60 - starttime) / 60)+1
                    #print(tmpind,len(segs))
                    for i in range(tmpind,len(segs)):
                        datagrouped.append({"TimeSeconds": begin + (i-tmpind) * 60, "bytes": int(segs[i])})
                    break
        with open(filename2, 'rb') as f:
            for line in f:
                segs = line.split(",")
                tmpip = int(segs[0])
                if(tmpip!=ipint):
                    continue
                else:
                    tmpind = int((end - endfile * 24 * 60 * 60 - starttime) / 60)+1
                    #print(1,tmpind)
                    tmpst = len(datagrouped)
                    for i in range(1,tmpind):
                        datagrouped.append({"TimeSeconds": begin + (i+tmpst-1) * 60, "bytes": int(segs[i])})
                    break
    return datagrouped

def timematch_stack():
    global notematch_num
    notematch_num={}
    for i in range(len(timematchnode)):
        for j in range(len(timematchnode[i])):
            if(timematchnode[i][j] in notematch_num):
                notematch_num[timematchnode[i][j]]=notematch_num[timematchnode[i][j]]+1
            else:
                notematch_num[timematchnode[i][j]]=1
timematch_stack()


#======================timeline func=============================
class initTimeline(tornado.web.RequestHandler):
  def get(self):
    #初始化时间轴
    evt_unpacked = {'day':daycnt , 'hour':hourcnt,'minute': minucnt }
    evt = json.dumps(evt_unpacked)
    self.write(evt)

class changeType(tornado.web.RequestHandler):
  def get(self):
    #时间轴改变类型：端口或协议
    global curtype
    curtype = json.loads(self.get_argument('type'))
    #global daycnt, hourcnt, minucnt
    daycnt = calcu_tl_day(curtype,tl_pro,tl_port)
    hourcnt = calcu_tl_hour(curday, curtype,tl_pro,tl_port)
    minucnt = calcu_tl_minu(curday, curhour, curtype,tl_pro,tl_port)
    evt_unpacked = {'day':daycnt , 'hour':hourcnt,'minute': minucnt }
    evt = json.dumps(evt_unpacked)
    self.write(evt)

class changeDay(tornado.web.RequestHandler):
  def get(self):
    #时间轴点击日或小时，更新数据
    global selectedtime
    global curday, curhour, curminu
    curday = json.loads(self.get_argument('day'))
    curhour = json.loads(self.get_argument('hour'))
    curminu = json.loads(self.get_argument('minute'))
    selectedtime=inittime+curday*24*60*60+curhour*60*60+curminu*60
    print("selectedtime",selectedtime)
    global daycnt, hourcnt, minucnt
    daycnt = calcu_tl_day(curtype,tl_pro,tl_port)
    hourcnt = calcu_tl_hour(curday, curtype,tl_pro,tl_port)
    minucnt = calcu_tl_minu(curday, curhour, curtype,tl_pro,tl_port)
    evt_unpacked = {'day': daycnt, 'hour': hourcnt, 'minute': minucnt}
    evt = json.dumps(evt_unpacked)
    self.write(evt)

class updateByMinute(tornado.web.RequestHandler):
  def get(self):
    #实时按分钟更新
    global selectedtime, nowtime
    global curday, curhour, curminu
    nowtime=nowtime+60
    selectedtime=nowtime
    curday, curhour, curminu = getcurtimeindex(selectedtime,starttime)
    cntDB2Timeline(selectedtime, selectedtime + 60)
    print("updateByMinute",selectedtime, selectedtime + 60)
    global daycnt, hourcnt, minucnt
    daycnt = calcu_tl_day(curtype,tl_pro,tl_port)
    hourcnt = calcu_tl_hour(curday, curtype,tl_pro,tl_port)
    minucnt = calcu_tl_minu(curday, curhour, curtype,tl_pro,tl_port)
    #print(minucnt[len(minucnt)-1])
    evt_unpacked = {'day': daycnt, 'hour': hourcnt, 'minute': minucnt}
    evt = json.dumps(evt_unpacked)
    self.write(evt)

class selectSoinnNode(tornado.web.RequestHandler):
  def get(self):
    #type = str(json.loads(self.get_argument('type')))
    id = json.loads(self.get_argument('nodeid'))
    print("selectSoinnNode",type,id)
    matchtime = []
    for j in range(len(timematchnode)):
        for k in range(len(timematchnode[j])):
            tmpid=int(timematchnode[j][k].split("_")[1])
            if (int(id)==tmpid):
                matchtime.append(starttime + j * 60)
    evt_unpacked = {'time': matchtime}
    evt = json.dumps(evt_unpacked)
    self.write(evt)


#======================soinn=============================
class init_soinn(tornado.web.RequestHandler):
  def get(self):
    evt_unpacked = {'nodes': nodes,'links':links}
    evt = json.dumps(evt_unpacked)
    self.write(evt)

class filterSoinnNode(tornado.web.RequestHandler):
  def get(self):
    st = int(json.loads(self.get_argument('starttime')))
    et = int(json.loads(self.get_argument('endtime')))
    #print(st,et)
    startindex=int((st-starttime)/60)
    endindex=int((et-starttime)/60)
    #print(startindex, endindex)
    matchid=timematchnode[startindex:endindex]
    nowfeat=exist_feature[startindex:endindex]
    distance=[]
    for k in range(len(matchid)):
        tmpdis = []
        for j in range(len(matchid[k])):
            tmptype=matchid[k][j].split("_")[0]
            tmpid=int(matchid[k][j].split("_")[1])
            tmpdis.append(LA.norm(nowfeat[k] - soinn_node[tmpid]))
        distance.append(tmpdis)
    evt_unpacked = {'nodes': matchid,'distance':distance}
    evt = json.dumps(evt_unpacked)
    self.write(evt)

class modifySoinn(tornado.web.RequestHandler):
  def get(self):
    evt_unpacked = {'nodes': []}
    evt = json.dumps(evt_unpacked)
    self.write(evt)


#======================statistic view=============================
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        super(DecimalEncoder, self).default(o)

class statisticdata(tornado.web.RequestHandler):
  def get(self):
    begin = int(json.loads(self.get_argument('starttime')))
    end = int(json.loads(self.get_argument('endtime')))
    querytype = int(json.loads(self.get_argument('querytype')))
    iptype = int(json.loads(self.get_argument('iptype')))
    sql=""
    for i in range(len(timesplitfile)):
        if(begin>=int(timesplitfile[i][1]) and begin<=int(timesplitfile[i][2])):
            beginfile=timesplitfile[i][0]
            break
    for i in range(len(timesplitfile)):
        if(end>int(timesplitfile[i][1]) and end<=int(timesplitfile[i][2])+1):
            endfile=timesplitfile[i][0]
            break
    if beginfile==endfile:
        if querytype==0:
            if iptype==0:
                sql = "SELECT count(*) as cnt,sum(firstSeenSrcTotalBytes) as bytes,firstSeenSrcIP as ip FROM "+beginfile+" where TimeSeconds>=%s and TimeSeconds < %s"+queryprecondition+"group by firstSeenSrcIP order by cnt"
            else:
                sql = "SELECT count(*) as cnt,sum(firstSeenDestTotalBytes) as bytes,firstSeenDestIP as ip FROM "+beginfile+" where TimeSeconds>=%s and TimeSeconds < %s"+queryprecondition+"group by firstSeenDestIP order by cnt"
        elif querytype==1:
            if iptype == 0:
                sql = "SELECT count(*) as cnt,firstSeenDestPort as port,firstSeenSrcIP as ip FROM "+beginfile+" where TimeSeconds>=%s and TimeSeconds < %s"+queryprecondition+"group by firstSeenDestPort,firstSeenSrcIP order by cnt"
            else:
                sql = "SELECT count(*) as cnt,firstSeenDestPort as port,firstSeenDestIP as ip FROM "+beginfile+" where TimeSeconds>=%s and TimeSeconds < %s"+queryprecondition+"group by firstSeenDestPort,firstSeenDestIP order by cnt"
        elif querytype==2:
            if iptype == 0:
                sql = "SELECT count(*) as cnt,sum(firstSeenSrcTotalBytes) as bytes,firstSeenSrcIP as ip FROM " + beginfile + " where TimeSeconds>=%s and TimeSeconds < %s"+queryprecondition+"group by firstSeenSrcIP order by bytes"
            else:
                sql = "SELECT count(*) as cnt,sum(firstSeenDestTotalBytes) as bytes,firstSeenDestIP as ip FROM " + beginfile + " where TimeSeconds>=%s and TimeSeconds < %s"+queryprecondition+"group by firstSeenDestIP order by bytes"
        elif querytype == 3:
            if iptype == 0:
                sql = "SELECT sum(firstSeenSrcTotalBytes) as bytes,firstSeenDestPort as port,firstSeenSrcIP as ip FROM " + beginfile + " where TimeSeconds>=%s and TimeSeconds < %s"+queryprecondition+"group by firstSeenDestPort,firstSeenSrcIP order by bytes"
            else:
                sql = "SELECT sum(firstSeenDestTotalBytes) as bytes,firstSeenDestPort as port,firstSeenDestIP as ip FROM " + beginfile + " where TimeSeconds>=%s and TimeSeconds < %s"+queryprecondition+"group by firstSeenDestPort,firstSeenDestIP order by bytes"
        elif querytype == 4:
            if iptype == 0:
                sql = "SELECT count(*) as cnt,firstSeenDestPort as port,firstSeenSrcIP as ip FROM " + beginfile + " where TimeSeconds>=%s and TimeSeconds < %s"+queryprecondition+"group by firstSeenDestPort,firstSeenSrcIP order by firstSeenDestPort"
            else:
                sql = "SELECT count(*) as cnt,firstSeenDestPort as port,firstSeenDestIP as ip FROM " + beginfile + " where TimeSeconds>=%s and TimeSeconds < %s"+queryprecondition+"group by firstSeenDestPort,firstSeenDestIP order by firstSeenDestPort"
        elif querytype == 5:
            if iptype == 0:
                sql = "SELECT sum(firstSeenSrcTotalBytes) as bytes,firstSeenDestPort as port,firstSeenSrcIP as ip FROM " + beginfile + " where TimeSeconds>=%s and TimeSeconds < %s"+queryprecondition+"group by firstSeenDestPort,firstSeenSrcIP order by firstSeenDestPort"
            else:
                sql = "SELECT sum(firstSeenDestTotalBytes) as bytes,firstSeenDestPort as port,firstSeenDestIP as ip FROM " + beginfile + " where TimeSeconds>=%s and TimeSeconds < %s"+queryprecondition+"group by firstSeenDestPort,firstSeenDestIP order by firstSeenDestPort"

    else:
        if querytype == 0:
            if iptype == 0:
                sql = "SELECT count(*) as cnt,sum(firstSeenSrcTotalBytes) as bytes,firstSeenSrcIP as ip FROM " + beginfile + " where TimeSeconds>=%s"+queryprecondition+"group by firstSeenSrcIP"+ \
                      " union SELECT count(*) as cnt,sum(firstSeenSrcTotalBytes) as bytes,firstSeenSrcIP as ip FROM " + endfile + " where TimeSeconds < %s"+queryprecondition+"group by firstSeenSrcIP order by cnt"
            else:
                sql = "SELECT count(*) as cnt,sum(firstSeenDestTotalBytes) as bytes,firstSeenDestIP as ip FROM " + beginfile + " where TimeSeconds>=%s"+queryprecondition+"group by firstSeenDestIP"+ \
                      " union SELECT count(*) as cnt,sum(firstSeenDestTotalBytes) as bytes,firstSeenDestIP as ip FROM " + endfile + " where TimeSeconds < %s"+queryprecondition+"group by firstSeenDestIP order by cnt"
        elif querytype == 1:
            if iptype == 0:
                sql = "SELECT count(*) as cnt,firstSeenDestPort as port,firstSeenSrcIP as ip FROM " + beginfile + " where TimeSeconds>=%s"+queryprecondition+"group by firstSeenDestPort,firstSeenSrcIP"+ \
                      " union SELECT count(*) as cnt,firstSeenDestPort as port,firstSeenSrcIP as ip FROM " + endfile + " where TimeSeconds < %s"+queryprecondition+"group by firstSeenDestPort,firstSeenSrcIP order by cnt"
            else:
                sql = "SELECT count(*) as cnt,firstSeenDestPort as port,firstSeenDestIP as ip FROM " + beginfile + " where TimeSeconds>=%s"+queryprecondition+"group by firstSeenDestPort,firstSeenDestIP"+ \
                      " union SELECT count(*) as cnt,firstSeenDestPort as port,firstSeenDestIP as ip FROM " + endfile + " where TimeSeconds < %s"+queryprecondition+"group by firstSeenDestPort,firstSeenDestIP order by cnt"
        elif querytype == 2:
            if iptype == 0:
                sql = "SELECT count(*) as cnt,sum(firstSeenSrcTotalBytes) as bytes,firstSeenSrcIP as ip FROM " + beginfile + " where TimeSeconds>=%s"+queryprecondition+"group by firstSeenSrcIP"+ \
                      " union SELECT count(*) as cnt,sum(firstSeenSrcTotalBytes) as bytes,firstSeenSrcIP as ip FROM " + endfile + " where TimeSeconds < %s"+queryprecondition+"group by firstSeenSrcIP order by bytes"
            else:
                sql = "SELECT count(*) as cnt,sum(firstSeenDestTotalBytes) as bytes,firstSeenDestIP as ip FROM " + beginfile + " where TimeSeconds>=%s"+queryprecondition+"group by firstSeenDestIP "+ \
                      " union SELECT count(*) as cnt,sum(firstSeenDestTotalBytes) as bytes,firstSeenDestIP as ip FROM " + endfile + " where TimeSeconds < %s"+queryprecondition+"group by firstSeenDestIP order by bytes"
        elif querytype == 3:
            if iptype == 0:
                sql = "SELECT sum(firstSeenSrcTotalBytes) as bytes,firstSeenDestPort as port,firstSeenSrcIP as ip FROM " + beginfile + " where TimeSeconds>=%s"+queryprecondition+"group by firstSeenDestPort,firstSeenSrcIP"+ \
                      " union SELECT sum(firstSeenSrcTotalBytes) as bytes,firstSeenDestPort as port,firstSeenSrcIP as ip FROM " + endfile + " where TimeSeconds < %s"+queryprecondition+"group by firstSeenDestPort,firstSeenSrcIP order by bytes"
            else:
                sql = "SELECT sum(firstSeenDestTotalBytes) as bytes,firstSeenDestPort as port,firstSeenDestIP as ip FROM " + beginfile + " where TimeSeconds>=%s"+queryprecondition+"group by firstSeenDestPort,firstSeenDestIP"+ \
                      " union SELECT sum(firstSeenDestTotalBytes) as bytes,firstSeenDestPort as port,firstSeenDestIP as ip FROM " + endfile + " where TimeSeconds < %s"+queryprecondition+"group by firstSeenDestPort,firstSeenDestIP order by bytes"
        elif querytype == 4:
            if iptype == 0:
                sql = "SELECT count(*) as cnt,firstSeenDestPort as port,firstSeenSrcIP as ip FROM " + beginfile + " where TimeSeconds>=%s group by firstSeenDestPort,firstSeenSrcIP"+ \
                      " union SELECT count(*) as cnt,firstSeenDestPort as port,firstSeenSrcIP as ip FROM " + endfile + " where TimeSeconds < %s group by firstSeenDestPort,firstSeenSrcIP order by firstSeenDestPort"
            else:
                sql = "SELECT count(*) as cnt,firstSeenDestPort as port,firstSeenDestIP as ip FROM " + beginfile + " where TimeSeconds>=%s group by firstSeenDestPort,firstSeenDestIP"+ \
                      " union SELECT count(*) as cnt,firstSeenDestPort as port,firstSeenDestIP as ip FROM " + endfile + " where TimeSeconds < %s group by firstSeenDestPort,firstSeenDestIP order by firstSeenDestPort"
        elif querytype == 5:
            if iptype == 0:
                sql = "SELECT sum(firstSeenSrcTotalBytes) as bytes,firstSeenDestPort as port,firstSeenSrcIP as ip FROM " + beginfile + " where TimeSeconds>=%s"+queryprecondition+"group by firstSeenDestPort,firstSeenSrcIP" + \
                      " union SELECT sum(firstSeenSrcTotalBytes) as bytes,firstSeenDestPort as port,firstSeenSrcIP as ip FROM " + endfile + " where TimeSeconds < %s"+queryprecondition+"group by firstSeenDestPort,firstSeenSrcIP order by firstSeenDestPort"
            else:
                sql = "SELECT sum(firstSeenDestTotalBytes) as bytes,firstSeenDestPort as port,firstSeenDestIP as ip FROM " + beginfile + " where TimeSeconds>=%s"+queryprecondition+"group by firstSeenDestPort,firstSeenDestIP" + \
                      " union SELECT sum(firstSeenDestTotalBytes) as bytes,firstSeenDestPort as port,firstSeenDestIP as ip FROM " + endfile + " where TimeSeconds < %s"+queryprecondition+"group by firstSeenDestPort,firstSeenDestIP order by firstSeenDestPort"

    print(sql)
    data= db.query(sql, begin, end)
    #datalist = [str(row[0]) for row in data]
    #print(data)
    evt_unpacked = {'data': data}
    evt = json.dumps(evt_unpacked, cls=DecimalEncoder)
    self.write(evt)
#======================net force view=============================
class forcedata(tornado.web.RequestHandler):
  def get(self):
    begin = int(json.loads(self.get_argument('starttime')))
    end = int(json.loads(self.get_argument('endtime')))
    sql=""
    for i in range(len(timesplitfile)):
        if(begin>=int(timesplitfile[i][1]) and begin<=int(timesplitfile[i][2])):
            beginfile=timesplitfile[i][0]
            break
    for i in range(len(timesplitfile)):
        if(end>int(timesplitfile[i][1]) and end<=int(timesplitfile[i][2])+1):
            endfile=timesplitfile[i][0]
            break
    if beginfile==endfile:
        sql = "SELECT count(*) as cnt,sum(firstSeenSrcTotalBytes) as srcbytes,sum(firstSeenDestTotalBytes) as dstbytes,firstSeenSrcIP as srcip,firstSeenDestIP as dstip FROM " + beginfile + " where TimeSeconds >= %s and TimeSeconds < %s"+queryprecondition+"group by firstSeenSrcIP,firstSeenDestIP"
    else:
        sql = "SELECT count(*) as cnt,sum(firstSeenSrcTotalBytes) as srcbytes,sum(firstSeenDestTotalBytes) as dstbytes,firstSeenSrcIP as srcip,firstSeenDestIP as dstip FROM " + beginfile + " where TimeSeconds >= %s"+queryprecondition+"group by firstSeenSrcIP,firstSeenDestIP" + \
              " union SELECT count(*) as cnt,sum(firstSeenSrcTotalBytes) as srcbytes,sum(firstSeenDestTotalBytes) as dstbytes,firstSeenSrcIP as srcip,firstSeenDestIP as dstip FROM " + endfile + " where TimeSeconds < %s"+queryprecondition+"group by firstSeenSrcIP,firstSeenDestIP"
    print(sql)
    data = db.query(sql, begin, end)
    nodes = []
    nodesbytes = []
    links = []

    for i in range(len(data)):
        if (data[i]["srcip"] in nodes):
            tmpsrcind = nodes.index(data[i]["srcip"])
            nodesbytes[tmpsrcind]["src"] = nodesbytes[tmpsrcind]["src"] + int(data[i]["srcbytes"])
        else:
            nodes.append(data[i]["srcip"])
            tmpsrcind = len(nodes) - 1
            nodesbytes.append({"ip": int(data[i]["srcip"]), "id": tmpsrcind, "src": int(data[i]["srcbytes"]), "dst": 0})
        if (data[i]["dstip"] in nodes):
            tmpdstind = nodes.index(data[i]["dstip"])
            nodesbytes[tmpdstind]["dst"] = nodesbytes[tmpdstind]["dst"] + int(data[i]["dstbytes"])
        else:
            nodes.append(data[i]["dstip"])
            tmpdstind = len(nodes) - 1
            nodesbytes.append({"ip": int(data[i]["dstip"]), "id": tmpdstind, "src": 0, "dst": int(data[i]["dstbytes"])})
        links.append({"source": tmpsrcind, "target": tmpdstind, "cnt": int(data[i]["cnt"])})
    evt_unpacked = {'nodes': nodesbytes, 'links': links}
    evt = json.dumps(evt_unpacked)
    self.write(evt)

#======================important IP=============================
class getentropy(tornado.web.RequestHandler):
  def get(self):
    #begin = int(json.loads(self.get_argument('starttime')))
    end = int(json.loads(self.get_argument('endtime')))
    endind = int((end - starttime) / 60) + 1
    beginind = endind - 60
    if (beginind < 0):
        beginind = 0
    tmpdata = exist_feature_origin[beginind:endind]
    tmpsrcip_entropy = tmpdata[:, 4:5].reshape(1, 60)
    tmpdstip_entropy = tmpdata[:, 6:7].reshape(1, 60)
    tmpsrcport_entropy = tmpdata[:, 8:9].reshape(1, 60)
    tmpdstport_entropy = tmpdata[:, 10:11].reshape(1, 60)
    evt_unpacked = {'srcip': tmpsrcip_entropy[0].tolist(), 'dstip': tmpdstip_entropy[0].tolist(), 'srcport': tmpsrcport_entropy[0].tolist(),
                    'dstport': tmpdstport_entropy[0].tolist()}
    evt = json.dumps(evt_unpacked)
    self.write(evt)

class getipsbytes(tornado.web.RequestHandler):
  def get(self):
    iparr = json.loads(self.get_argument('iparr'))
    iptypearr = json.loads(self.get_argument('iptypearr'))
    end = int(json.loads(self.get_argument('endtime')))

    evt_unpacked={}
    for i in range(len(iparr)):
        tmpdata=getipbytes2(iparr[i], iptypearr[i], end)
        evt_unpacked[str(iparr[i])]=tmpdata
    evt = json.dumps(evt_unpacked, cls=DecimalEncoder)
    self.write(evt)

#def getimport():
class getimport(tornado.web.RequestHandler):
  def get(self):
    '''
    maxipnum=5

    end = int(json.loads(self.get_argument('endtime')))+60
    #end=1365078600+60
    begin = end - 60
    if (begin < 0):
        begin = 0
    tmpind = int((end - starttime) / 60) -1
    originfeature=exist_feature[tmpind]

    for i in range(len(timesplitfile)):
        if (begin >= int(timesplitfile[i][1]) and begin <= int(timesplitfile[i][2])):
            beginfile = timesplitfile[i][0]
            break
    #查询流量最高的5个源IP和目的IP
    #查询一分钟内总数据
    sql1 ="SELECT firstSeenSrcIP,sum(firstSeenSrcTotalBytes) as srcbyte FROM " + beginfile + " where TimeSeconds>=%s and TimeSeconds<%s" + queryprecondition + "group by firstSeenSrcIP order by srcbyte desc limit "+str(maxipnum)
    sql2 ="SELECT firstSeenDestIP,sum(firstSeenDestTotalBytes) as dstbyte FROM " + beginfile + " where TimeSeconds>=%s and TimeSeconds<%s" + queryprecondition + "group by firstSeenDestIP order by dstbyte desc limit "+str(maxipnum)
    sql3 ="SELECT * FROM " + beginfile + " where TimeSeconds>=%s and TimeSeconds<%s" + queryprecondition + "order by TimeSeconds"
    print("getimport",begin, end)
    datasrc = db.query(sql1, begin, end)
    datadst = db.query(sql2, begin, end)
    if(nowtime==begin and len(newdata_minute)>0):
        dataall=newdata_minute
        #dataall2=(db.query(sql3, begin, end))
        print("exist")
    else:
        dataall = db.query(sql3, begin, end)
    #求去掉特定IP后新的特征值
    newfeatures=[]
    for i in range(len(datasrc)):
        tmpfeat0,tmpfeat=generate_feature_ignore(dataall,datasrc[i]["firstSeenSrcIP"])
        newfeatures.append(tmpfeat)
    for i in range(len(datadst)):
        tmpfeat0,tmpfeat=generate_feature_ignore(dataall,datadst[i]["firstSeenDestIP"])
        newfeatures.append(tmpfeat)
    # 分别求使得特征值变化最多的2个IP
    maxval = 0
    maxval2 = 0
    maxind = -1
    maxind2 = -1
    # 找出与p_data[i]最相似的两个神经元
    for i in xrange(len(newfeatures)):
        dis = LA.norm(newfeatures[i] - originfeature)
        #print(dis)
        if dis > maxval:
            maxval2 = maxval
            maxind2 = maxind
            maxval = dis
            maxind = i
        elif dis > maxval2:
            maxval2 = dis
            maxind2 = i
    print(maxind, maxind2)
    # 求这两个IP过去60分钟的流量
    evt_unpacked={}
    if(maxind!=-1):
        if(maxind<len(datasrc)):
            tmpip1=datasrc[maxind]["firstSeenSrcIP"]
            tmpip1type="src"
        else:
            tmpip1 = datadst[maxind-len(datasrc)]["firstSeenDestIP"]
            tmpip1type = "dst"
        ipdata1 = getipbytes(tmpip1, tmpip1type, end - 60)
        evt_unpacked["ip1"]=tmpip1
        evt_unpacked["ip1type"] = tmpip1type
        evt_unpacked["ip1data"]=ipdata1
    else:
        evt_unpacked["ip1"] = -1
        evt_unpacked["ip1data"] = []
    if (maxind2 != -1):
        if (maxind2< len(datasrc)):
            tmpip2 = datasrc[maxind2]["firstSeenSrcIP"]
            tmpip2type = "src"
        else:
            tmpip2 = datadst[maxind2 - len(datasrc)]["firstSeenDestIP"]
            tmpip2type = "dst"
        ipdata2 = getipbytes(tmpip2, tmpip2type, end - 60)
        evt_unpacked["ip2"] = tmpip2
        evt_unpacked["ip2type"] = tmpip2type
        evt_unpacked["ip2data"] = ipdata2
    else:
        evt_unpacked["ip2"] = -1
        evt_unpacked["ip2data"] = []
    #print("kkk")
    evt = json.dumps(evt_unpacked)
    self.write(evt)

    '''
    end = int(json.loads(self.get_argument('endtime'))) + 60
    tmpind = int((end - starttime) / 60) - 1
    tmpip1=importantips[tmpind][0]
    tmpip1type=importantips[tmpind][1]
    tmpip2 = importantips[tmpind][2]
    tmpip2type = importantips[tmpind][3]
    evt_unpacked={}
    if (tmpip1 != -1):
        ipdata1 = getipbytes2(tmpip1, tmpip1type, end - 60)
        evt_unpacked["ip1"] = tmpip1
        evt_unpacked["ip1type"] = tmpip1type
        evt_unpacked["ip1data"] = ipdata1
    else:
        evt_unpacked["ip1"] = -1
        evt_unpacked["ip1data"] = []
    if (tmpip2 != -1):
        ipdata2 = getipbytes2(tmpip2, tmpip2type, end - 60)
        evt_unpacked["ip2"] = tmpip2
        evt_unpacked["ip2type"] = tmpip2type
        evt_unpacked["ip2data"] = ipdata2
    else:
        evt_unpacked["ip2"] = -1
        evt_unpacked["ip2data"] = []
        # print("kkk")
    evt = json.dumps(evt_unpacked)
    self.write(evt)


#getimport()


class Application(tornado.web.Application):
  def __init__ (self):
    handlers = [
      (r'/initTimeline', initTimeline),
      (r'/changeType', changeType),
      (r'/changeDay', changeDay),
      (r'/updateByMinute', updateByMinute),
      (r'/selectSoinnNode', selectSoinnNode),
      (r'/init_soinn', init_soinn),
      (r'/filterSoinnNode', filterSoinnNode),
      (r'/modifySoinn', modifySoinn),
      (r'/statisticdata', statisticdata),
      (r'/forcedata', forcedata),
      (r'/getentropy', getentropy),
      (r'/getipsbytes', getipsbytes),
      (r'/getimport', getimport),
      (r'/(.*)', tornado.web.StaticFileHandler, {'path': client_file_root_path, 'default_filename': 'index.html'}) # fetch client files
    ]

    settings = {
      'static_path': 'static',
      'debug': True
    }

    tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == '__main__':
  tornado.options.parse_command_line()
  print('server running at 127.0.0.1:%d ...'%(tornado.options.options.port))

  app = Application()
  http_server = tornado.httpserver.HTTPServer(app)
  http_server.listen(options.port)
  tornado.ioloop.IOLoop.instance().start()

