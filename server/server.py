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
import operator
import copy
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
soinn_node_embedded = TSNE(n_components=2,learning_rate=380).fit_transform(soinn_node)

print("init distance")
soinn_distance=calcu_dis(soinn_node)
print("init uncertainty")
typearr = np.array(["normal", "abnormal", "uncertain"])
nodenum=soinn_node.shape[0]
soinn_certainty=np.zeros((nodenum,3))#normal,abnormal,uncertain
ceratinty_history=[]
type_history=[]
labelednode_history=[]

for i in range(len(soinn_certainty)):
    soinn_certainty[i][2]=1
print("connect2json")
nodes, links=connect2json(soinn_node,soinn_node_embedded,soinn_connection,soinn_age,soinn_wincnt,soinn_threshold)
def nodesinthre():
    #把wincnt不映射到节点获胜次数 而是映射到节点阈值内的其他节点个数
    for i in range(len(soinn_node)):
        tmpnum=0
        for j in range(len(soinn_node)):
            if soinn_distance[i][j]<soinn_threshold[i] and j!=i:
                tmpnum=tmpnum+1
        nodes[i]["wincnt"]=tmpnum
nodesinthre()
def classnodes():
    #为了chaeck是否把相似的节点聚在了一起 提前label节点类型
    global nodes
    for i in range(len(nodes)):
        tmptimes=[]
        for j in range(len(timematchnode)):
            for k in range(len(timematchnode[j])):
                if int(timematchnode[j][k].split("_")[1])==i:
                    tmptimes.append(j)
        normalnum=0
        abnormalnum=0
        for j in range(len(tmptimes)):
            if(timelabels[tmptimes[j]]==0):
                normalnum=normalnum+1
            else:
                abnormalnum=abnormalnum+1

        if normalnum+abnormalnum==0:
            nodes[i]["type"] = "normal"
        elif abnormalnum/float(normalnum+abnormalnum)>0.1:
            nodes[i]["type"]="abnormal"
        else:
            nodes[i]["type"] = "normal"
        print(i,normalnum, abnormalnum,nodes[i]["type"])
#classnodes()

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




#更新隶属度
def updateMembershipValue(k,cluster_id,cluster_type):
#    p = float(2/(m-1))

    #soinn_certainty_new
    soinn_certainty_new = np.zeros((nodenum, 3))
    for i in range(len(soinn_certainty_new)):
        for j in range(3):
            soinn_certainty_new[i][j] = soinn_certainty[i][j]
    #遍历每个节点 求各类的隶属度
    for i in range(len(soinn_node)):
        #label过的节点不动
        if nodes[i]["labeled"]==1:
            continue
        cluster_type_tmp=copy.deepcopy(cluster_type)
        distances=[]
        for j in range(k):
            distances.append(soinn_distance[i][cluster_id[j]])
        #加入在阈值范围内的节点作为额外的center
        #更新type distances

        for j in range(len(soinn_node)):
            if soinn_distance[i][j]<soinn_threshold[i] and j!=i and not(j in cluster_id):
                #if i==71:print(nodes[j])
                cluster_type_tmp.append(nodes[j]["type"])
                tmptypeind=np.where(typearr == nodes[j]["type"])[0][0]
                if(soinn_certainty[j][tmptypeind]==0):
                    print(nodes[j],tmptypeind)
                tmpdis=soinn_distance[i][j]/float(soinn_certainty[j][tmptypeind])
                distances.append(tmpdis)
            #if len(cluster_type_tmp)-len(cluster_type)>3:
            #    break

        #如果阈值范围内没有其他节点，加入最近的节点
        if(len(cluster_type_tmp)==len(cluster_type)):
            nearestnodeid=-1
            nearestdis=10000
            for j in range(len(soinn_distance)):
                if j!=i and soinn_distance[i][j]<nearestdis and not(j in cluster_id):
                    nearestdis=soinn_distance[i][j]
                    nearestnodeid=j
            cluster_type_tmp.append(nodes[nearestnodeid]["type"])
            tmptypeind = np.where(typearr == nodes[nearestnodeid]["type"])[0][0]
            tmpdis = soinn_distance[i][nearestnodeid]/float(soinn_certainty[nearestnodeid][tmptypeind])
            distances.append(tmpdis)

        tmpcertainty=[0,0,0]
        #统计隶属度

        kk = len(cluster_type_tmp)
        for j in range(kk):
            den = sum([math.pow(distances[j]/float(distances[c]), 2) for c in range(kk)])
            tmptype=cluster_type_tmp[j]
            tmptypeind = np.where(typearr == tmptype)[0][0]
            tmpcertainty[tmptypeind] = tmpcertainty[tmptypeind]+1/float(den)
        tmpsum=np.sum(tmpcertainty)
        for j in range(len(tmpcertainty)):
            soinn_certainty_new[i][j]=tmpcertainty[j]/float(tmpsum)
    totaldis=0
    for i in range(len(soinn_certainty_new)):
        for j in range(3):
            totaldis=totaldis+(soinn_certainty_new[i][j]-soinn_certainty[i][j])*(soinn_certainty_new[i][j]-soinn_certainty[i][j])
    return soinn_certainty_new,totaldis

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        super(DecimalEncoder, self).default(o)

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
def getchangednodes():
    nodesarr=[]
    if len(type_history)<2:
        return nodesarr
    else:
        nowtype = type_history[-1]
        pretype = type_history[-2]
        for i in range(len(nowtype)):
            if(nowtype[i]=="normal" and pretype[i]=="abnormal") or (nowtype[i]=="abnormal" and pretype[i]=="normal"):
                nodesarr.append(i)
        return nodesarr

class init_soinn(tornado.web.RequestHandler):
  def get(self):
    evt_unpacked = {'nodes': nodes,'links':links,'distance':soinn_distance.tolist(),'changednodes':getchangednodes(),'labelednode':labelednode_history}
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

class nodeAffect(tornado.web.RequestHandler):
  def get(self):
    nodeid = int(json.loads(self.get_argument('nodeid')))
    centernodes = json.loads(self.get_argument('labelednodes'))
    k = len(centernodes)
    cluster_id = []
    cluster_type = []
    distances = []
    affectnodes=[]
    incenter=0
    for i in range(len(centernodes)):
        if(centernodes[i]["id"]==nodeid):
            incenter=1
            break
    if incenter==0:
        for i in range(k):
            cluster_id.append(int(centernodes[i]["id"]))
            cluster_type.append(centernodes[i]["type"])
        for j in range(k):
            distances.append(soinn_distance[nodeid][cluster_id[j]])

        for j in range(k):
            den = sum([math.pow(distances[j] / float(distances[c]), 2) for c in range(k)])
            den=1 / float(den)
            print(cluster_id[j],den)
            #if den>1/float(k):
            #如果影响大于均值
            affectnodes.append([cluster_id[j],den])
    evt_unpacked = {'affectnodes': affectnodes}
    evt = json.dumps(evt_unpacked)
    self.write(evt)


class labelSoinn(tornado.web.RequestHandler):
  def get(self):
    type=0 #type=0 uncertain也有概率; type=1 uncertain没有概率
    lbnode=(json.loads(self.get_argument('labelednodes')))
    global labelednode_history
    labelednode_history.append(lbnode)
    centernodes=[]
    for i in range(len(labelednode_history)):
        centernodes.append(labelednode_history[i])
    #centernodes=json.loads(self.get_argument('labelednodes'))
    normalthre = float(json.loads(self.get_argument('normalthre')))
    abnormalthre = float(json.loads(self.get_argument('abnormalthre')))
    # 初始化聚类中心
    k = len(centernodes)
    cluster_id = []
    cluster_type = []
    for i in range(k):
        cluster_id.append(int(centernodes[i]["id"]))
        cluster_type.append(centernodes[i]["type"])
    # 更新label的节点
    for i in range(k):
        nodes[cluster_id[i]]["labeled"] = 1
        nodes[cluster_id[i]]["type"] = cluster_type[i]
        nodes[cluster_id[i]]["certainty"] = [0, 0, 0]
        soinn_certainty[cluster_id[i]] = [0, 0, 0]
        tmptypeind = np.where(typearr == cluster_type[i])[0][0]
        nodes[cluster_id[i]]["certainty"][tmptypeind] = 1
        soinn_certainty[cluster_id[i]][tmptypeind] = 1
    #聚类中心阈值内的点归为和聚类中心一类
    #如果一个点同时在多种聚类中心阈值内，根据距离求概率

    for i in range(len(soinn_distance)):
        if i in cluster_id:
            continue
        normal_min_dis = 1000
        normal_min_ind = -1
        abnormal_min_dis = 1000
        abnormal_min_ind = -1
        for j in range(k):
            tmpcenterind=cluster_id[j]
            if soinn_distance[i][tmpcenterind]<soinn_threshold[tmpcenterind]:
                if cluster_type[j]=="normal" and soinn_distance[i][tmpcenterind]<normal_min_dis:
                    normal_min_dis=soinn_distance[i][tmpcenterind]
                    normal_min_ind = tmpcenterind
                elif cluster_type[j]=="abnormal" and soinn_distance[i][tmpcenterind]<abnormal_min_dis:
                    abnormal_min_dis=soinn_distance[i][tmpcenterind]
                    abnormal_min_ind = tmpcenterind
        if normal_min_ind==-1 and abnormal_min_ind==-1:
            continue
        elif normal_min_ind!=-1 and abnormal_min_ind!=-1:
            tmpnormalperc=abnormal_min_dis/float(normal_min_dis+abnormal_min_dis)
            tmpabnormalperc=1-tmpnormalperc
            nodes[i]["certainty"] = [tmpnormalperc, tmpabnormalperc, 0]
            soinn_certainty[i]= [tmpnormalperc, tmpabnormalperc, 0]
            #if tmpnormalperc>tmpabnormalperc and tmpnormalperc>normalthre:
            if tmpnormalperc>normalthre:
                nodes[i]["type"] = "normal"
            #elif tmpabnormalperc>tmpnormalperc and tmpabnormalperc>abnormalthre:
            elif tmpabnormalperc>abnormalthre:
                nodes[i]["type"] = "abnormal"
            else:
                nodes[i]["type"] = "uncertain"
        elif normal_min_ind!=-1:
            tmpnormalperc = 1 - normal_min_dis / float(soinn_threshold[normal_min_ind])
            if tmpnormalperc>normalthre:
                nodes[i]["type"] = "normal"
            else:
                nodes[i]["type"] = "uncertain"
            nodes[i]["certainty"] = [tmpnormalperc, 0, 1-tmpnormalperc]
            soinn_certainty[i] = [tmpnormalperc, 0, 1-tmpnormalperc]
        else:
            tmpabnormalperc = 1 - abnormal_min_dis / float(soinn_threshold[abnormal_min_ind])
            if tmpabnormalperc>abnormalthre:
                nodes[i]["type"] = "abnormal"
            else:
                nodes[i]["type"] = "uncertain"
            nodes[i]["certainty"] = [0, tmpabnormalperc, 1-tmpabnormalperc]
            soinn_certainty[i] = [0, tmpabnormalperc, 1-tmpabnormalperc]

    #最多迭代10次
    for i in range(10):
        # 求解隶属矩阵
        soinn_certainty_new, totaldis = updateMembershipValue(k, cluster_id, cluster_type)
        print(totaldis)
        #更新隶属矩阵
        for i in range(len(soinn_certainty_new)):
            for j in range(3):
                soinn_certainty[i][j]=soinn_certainty_new[i][j]
            # 如果normal和abnormal都有可能 标记为其中一个 不考虑uncertain
            if type==1:
                if soinn_certainty_new[i][0]*soinn_certainty_new[i][1]*soinn_certainty_new[i][2]!=0:
                    soinn_certainty_new[i][0]=soinn_certainty_new[i][0]/(soinn_certainty_new[i][0]+soinn_certainty_new[i][1])
                    soinn_certainty_new[i][1]=soinn_certainty_new[i][1]/(soinn_certainty_new[i][0]+soinn_certainty_new[i][1])
                    soinn_certainty_new[i][2]=0
        # 求每个节点可能的类型
        for i in range(len(nodes)):
            # label过的节点不动
            if nodes[i]["labeled"] == 1:
                continue
            nodes[i]["certainty"][0] = soinn_certainty[i][0]
            nodes[i]["certainty"][1] = soinn_certainty[i][1]
            nodes[i]["certainty"][2] = soinn_certainty[i][2]
            tmpnormal = nodes[i]["certainty"][0]
            tmpabnormal = nodes[i]["certainty"][1]
            if type==1:
                if tmpnormal!=0 and tmpabnormal!=0:
                    # [a,b,0]
                    if tmpabnormal>0.5:
                        nodes[i]["type"] = "abnormal"
                    else:
                        nodes[i]["type"] = "normal"
                else:
                    if tmpnormal>normalthre:
                        # [a,0,c]
                        nodes[i]["type"] = "normal"
                    elif tmpabnormal>abnormalthre:
                        # [0,b,c]
                        nodes[i]["type"] = "abnormal"
                    else:
                        nodes[i]["type"] = "uncertain"
            else:
                if (tmpnormal > normalthre):
                    nodes[i]["type"] = "normal"
                elif (tmpabnormal > abnormalthre):
                    nodes[i]["type"] = "abnormal"
                else:
                    nodes[i]["type"] = "uncertain"
        if totaldis<0.01:
            break
    #更新timematchnode
    tmpresult=[]
    for i in range(len(timematchnode)):
        tmpresult.append(0)
        for j in range(len(timematchnode[i])):
            tmpid= int(timematchnode[i][j].split("_")[1])
            tmptype=nodes[tmpid]["type"]
            timematchnode[i][j]=tmptype+"_"+str(tmpid)
            if tmptype=="abnormal":
                tmpresult[len(tmpresult)-1]=1
    global timematchnode1
    timematchnode1 = np.array(timematchnode)
    #统计检测率
    totalnum=min(len(timelabels),len(tmpresult))
    normalnum=0
    tpnum=0#异常样本标记为异常的次数
    fpnum=0#正常样本误判为异常的次数
    for i in range(totalnum):
        if timelabels[i]==0:
            normalnum=normalnum+1
            if tmpresult[i]==1:
                fpnum=fpnum+1
        else:
            if tmpresult[i]==1:
                tpnum=tpnum+1
    #存储certainty历史
    global ceratinty_history,type_history
    ceratinty_now = []
    type_now=[]
    for i in range(len(nodes)):
        ceratinty_now.append(nodes[i]["certainty"])
        type_now.append(nodes[i]["type"])
    ceratinty_history.append(ceratinty_now)
    type_history.append(type_now)

    print("totalnum",totalnum,"normalnum",normalnum,"tpnum",tpnum,"fpnum",fpnum)
    evt_unpacked = {'nodes': nodes,'changednodes':getchangednodes(),'labelednode':labelednode_history}
    evt = json.dumps(evt_unpacked)
    self.write(evt)

class resetLayout(tornado.web.RequestHandler):
  def get(self):
    # 重新映射
    global soinn_node_embedded,nodes
    soinn_node_embedded = TSNE(n_components=2, learning_rate=380).fit_transform(soinn_node)
    # 更新nodes
    for i in range(len(nodes)):
        nodes[i]["feature"] = soinn_node_embedded[i].tolist()
    evt_unpacked = {'nodes': nodes,'links':links,'distance':soinn_distance.tolist()}
    evt = json.dumps(evt_unpacked)
    self.write(evt)

class getHistory(tornado.web.RequestHandler):
  def get(self):
    nodeid=int(json.loads(self.get_argument('nodeid')))
    nodehistory=[]
    for i in range(len(ceratinty_history)):
        nodehistory.append(ceratinty_history[i][nodeid])
    evt_unpacked = {'history': nodehistory}
    evt = json.dumps(evt_unpacked)
    self.write(evt)
#======================matrix=============================
def getmatrix(selectedid):
    timearr = []
    nodearr = [nodes[selectedid]]

    # 查找含有选中节点的对应时间
    for i in range(len(timematchnode)):
        for j in range(len(timematchnode[i])):
            tmpid = int(timematchnode[i][j].split("_")[1])
            if tmpid == selectedid:
                timearr.append(i)
    # 查找这些时间对应的其他节点
    for i in range(len(timearr)):
        tmparr = timematchnode[timearr[i]]
        for j in range(len(tmparr)):
            tmpid = int(tmparr[j].split("_")[1])
            if tmpid != selectedid:
                existflag = 0
                for k in range(len(nodearr)):
                    if nodearr[k]["id"] == tmpid:
                        existflag = 1
                        break
                if existflag == 0:
                    nodearr.append(nodes[tmpid])
    # 生成certainty矩阵
    matrix_certainty = np.zeros((len(nodearr), len(timearr)))
    # 遍历求certainty
    for i in range(len(timearr)):
        tmpnodesind = []
        for j in range(len(nodearr)):
            tmpstr = nodearr[j]["type"] + "_" + str(nodearr[j]["id"])
            if tmpstr in timematchnode[timearr[i]]:
                tmpnodesind.append(j)
        if len(tmpnodesind) == 1:
            tmpdis = LA.norm(nodearr[tmpnodesind[0]]["features_all"] - exist_feature[timearr[i]])
            tmpthre = nodearr[tmpnodesind[0]]["threshold"]
            matrix_certainty[tmpnodesind[0]][i] = tmpthre / float(tmpthre + tmpdis)
        else:
            tmpdis1 = LA.norm(nodearr[tmpnodesind[0]]["features_all"] - exist_feature[timearr[i]])
            tmpdis2 = LA.norm(nodearr[tmpnodesind[1]]["features_all"] - exist_feature[timearr[i]])
            matrix_certainty[tmpnodesind[0]][i] = tmpdis2 / float(tmpdis1 + tmpdis2)
            matrix_certainty[tmpnodesind[1]][i] = tmpdis1 / float(tmpdis1 + tmpdis2)
    return nodearr,timearr,matrix_certainty

class updateMatrix_node(tornado.web.RequestHandler):
  def get(self):
    print("updateMatrix_node")
    selectedid = int(json.loads(self.get_argument('nodeid')))
    if selectedid==-1:
        mincertainty=1
        #找certainty最小的节点
        for i in range(len(nodes)):
            if nodes[i]["type"]=="normal" and nodes[i]["certainty"][0]<mincertainty:
                mincertainty=nodes[i]["certainty"][0]
                selectedid=i
            elif nodes[i]["type"]=="abnormal" and nodes[i]["certainty"][1]<mincertainty:
                mincertainty=nodes[i]["certainty"][1]
                selectedid=i
        if selectedid==-1:
            selectedid=0

    nodearr, timearr, matrix_certainty=getmatrix(selectedid)
    print("updateMatrix_node end")
    evt_unpacked = {'nodes': nodearr,'times':timearr,'matrix':matrix_certainty.tolist()}
    evt = json.dumps(evt_unpacked)
    self.write(evt)

class updateMatrix_time(tornado.web.RequestHandler):
  def get(self):
    print("updateMatrix_time")
    timeind = int(json.loads(self.get_argument('timeind')))
    nodesid=[]
    for i in range(len(timematchnode[timeind])):
        tmpid = int(timematchnode[timeind][i].split("_")[1])
        nodesid.append(tmpid)
    selectedid=nodesid[0]

    nodearr, timearr, matrix_certainty=getmatrix(selectedid)
    print("updateMatrix_time end")
    evt_unpacked = {'nodes': nodearr,'times':timearr,'matrix':matrix_certainty.tolist()}
    evt = json.dumps(evt_unpacked)
    self.write(evt)

class labelTime(tornado.web.RequestHandler):
  def get(self):
    print("labelTime")
    labeledtimeind = int(json.loads(self.get_argument('labeledtimeind')))
    labeledtype = json.loads(self.get_argument('labeledtype'))
    #soinn加入新的节点
    global soinn_node, soinn_connection, soinn_wincnt, soinn_threshold, soinn_age
    soinn_node=soinn_node.tolist()
    soinn_node, soinn_connection, soinn_wincnt, soinn_threshold, soinn_age, tmpminind, tmpminind2=SOINN_addnode(exist_feature[labeledtimeind], soinn_node, soinn_connection, soinn_wincnt, soinn_threshold, soinn_age)
    soinn_node=np.array(soinn_node)
    #更新timematchnode和wincnt
    tmpnewind = len(soinn_node) - 1
    for i in range(len(timematchnode)):
        for j in range(len(timematchnode[i])):
            tmpid=int(timematchnode[i][j].split("_")[1])
            if tmpid==tmpminind or tmpid==tmpminind2:
                tmporigindis = LA.norm(exist_feature[i] - soinn_node[tmpid])
                newdis=LA.norm(exist_feature[i] - soinn_node[tmpnewind])
                if newdis<tmporigindis:
                    timematchnode[i][j]=labeledtype+"_"+str(tmpnewind)
                    soinn_wincnt[tmpid]=soinn_wincnt[tmpid]-1
                    soinn_wincnt[tmpnewind]=soinn_wincnt[tmpnewind]+1
    #重新映射
    soinn_node_embedded = TSNE(n_components=2, learning_rate=380).fit_transform(soinn_node)
    #更新nodes links
    global nodes,links
    #加入新节点
    nodes.append(
        {"id": tmpnewind, "wincnt": soinn_wincnt[tmpnewind], "features_all": exist_feature[labeledtimeind].tolist(), "feature": [],
         "threshold": soinn_threshold[tmpnewind], "type": labeledtype, "certainty": [0, 0, 0], "labeled": 1})
    if labeledtype=="normal":
        nodes[tmpnewind]["certainty"]=[1,0,0]
    else:
        nodes[tmpnewind]["certainty"] = [0,1,0]
    #删除多余的边
    #print(len(links))
    for i in range(len(links)):
        #print(i)
        if (links[i]["source"]==tmpminind and links[i]["target"]==tmpminind2) or (links[i]["source"]==tmpminind2 and links[i]["target"]==tmpminind):
            links = links[:i] + links[i+ 1:]
            break
    #加入边
    links.append({"source": tmpminind, "target": tmpnewind, "cnt": 1, "age": 1})
    links.append({"source": tmpminind2, "target": tmpnewind, "cnt": 1, "age": 1})
    #更新nodes
    for i in range(len(nodes)):
        nodes[i]["feature"]=soinn_node_embedded[i].tolist()
    #更新links
    for i in range(len(links)):
        links[i]["cnt"]=soinn_connection[links[i]["source"]][links[i]["target"]]
        links[i]["age"]=soinn_age[links[i]["source"]][links[i]["target"]]
    # 更新其他矩阵
    global soinn_certainty, soinn_distance
    soinn_certainty = np.row_stack((soinn_certainty, [0, 0, 0]))
    soinn_distance = np.row_stack((soinn_distance, np.zeros(soinn_distance.shape[1])))
    soinn_distance = np.column_stack((soinn_distance, np.zeros(soinn_distance.shape[0])))
    for i in range(len(soinn_node)):
        soinn_distance[tmpminind][i] = LA.norm(soinn_node[tmpminind] - soinn_node[i])
        soinn_distance[i][tmpminind] = soinn_distance[tmpminind][i]
        soinn_distance[tmpminind2][i] = LA.norm(soinn_node[tmpminind2] - soinn_node[i])
        soinn_distance[i][tmpminind2] = soinn_distance[tmpminind2][i]
        soinn_distance[tmpnewind][i] = LA.norm(soinn_node[tmpnewind] - soinn_node[i])
        soinn_distance[i][tmpnewind] = soinn_distance[tmpnewind][i]
    print("labelTime end")
    evt_unpacked = {}
    evt = json.dumps(evt_unpacked)
    self.write(evt)
#======================statistic view=============================

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
      (r'/nodeAffect', nodeAffect),
      (r'/labelSoinn', labelSoinn),
      (r'/getHistory', getHistory),
      (r'/resetLayout', resetLayout),
      (r'/updateMatrix_node', updateMatrix_node),
      (r'/updateMatrix_time', updateMatrix_time),
      (r'/labelTime', labelTime),
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

