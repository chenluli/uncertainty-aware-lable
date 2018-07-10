#! /usr/bin/python
# -*- coding:utf-8 -*-


import datetime
import time
import math
import numpy as np
import csv

def init_file(filepostfix,inittime,starttime,saveday,tlfile):
    #读取inittime时间点之前以及统计好的数据
    tl=[]
    for i in range(saveday):
        tl.append([])
    filetoread=[]
    for i in range(len(tlfile)):
        if(inittime>tlfile[i][1]):
            filetoread.append("../client/data/"+tlfile[i][0]+filepostfix)
        else:
            break
    for i in range(len(filetoread)):
        with open(filetoread[i], 'r') as file:
            csvReader = csv.reader(file)
            for line in csvReader:
                if int(line[0])>inittime:
                    return tl
                for j in range(len(line)):
                    line[j]=int(line[j].strip())
                tmpday=int((line[0]-starttime)/(24*60*60))
                tl[tmpday].append(line)
    return tl

def getcurtimeindex(t,starttime):
    #返回给定时间戳和最早时间之间相比是第几天，以及该时间戳最近的hour和minute
    curday=int((t-starttime)/(24*60*60))
    timeStamp = t-8*60*60
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%H:%M", timeArray)
    otherStyleTime=otherStyleTime.split(":")
    cur_hour=int(otherStyleTime[0])
    cur_minu=int(otherStyleTime[1])
    print(curday,cur_hour,cur_minu)
    return [curday,cur_hour,cur_minu]

def calcu_tl_day(type,tl_pro,tl_port):
    #tl_pro或tl_port文件的数据按日聚合
    daycnt = []
    if (int(type / 3) == 0):
        # 是protocal
        for i in range(len(tl_pro)):
            if(len(tl_pro[i])==0):return daycnt
            daycnt.append({"tm": tl_pro[i][0][0], "tcp": 0, "udp": 0, "others": 0})
            for j in range(len(tl_pro[i])):
                if (type == 0):  # all
                    daycnt[i]["tcp"] = daycnt[i]["tcp"] + tl_pro[i][j][1] + tl_pro[i][j][2]
                    daycnt[i]["udp"] = daycnt[i]["udp"] + tl_pro[i][j][3] + tl_pro[i][j][4]
                    daycnt[i]["others"] = daycnt[i]["others"] + tl_pro[i][j][5] + tl_pro[i][j][6]
                elif (type == 1):  # src
                    daycnt[i]["tcp"] = daycnt[i]["tcp"] + tl_pro[i][j][1]
                    daycnt[i]["udp"] = daycnt[i]["udp"] + tl_pro[i][j][3]
                    daycnt[i]["others"] = daycnt[i]["others"] + tl_pro[i][j][5]
                else:
                    daycnt[i]["tcp"] = daycnt[i]["tcp"] + tl_pro[i][j][2]
                    daycnt[i]["udp"] = daycnt[i]["udp"] + tl_pro[i][j][4]
                    daycnt[i]["others"] = daycnt[i]["others"] + tl_pro[i][j][6]
    else:
        #是port
        for i in range(len(tl_port)):
            if (len(tl_port[i]) == 0): return daycnt
            daycnt.append({"tm": tl_port[i][0][0], "ftp": 0, "ssh": 0, "mail":0,"http":0,"NetBIOS":0,"reflect":0,"others": 0})
            for j in range(len(tl_port[i])):
                if (type == 3):  # all
                    daycnt[i]["ftp"] = daycnt[i]["ftp"] + tl_port[i][j][1] + tl_port[i][j][2]
                    daycnt[i]["ssh"] = daycnt[i]["ssh"] + tl_port[i][j][3] + tl_port[i][j][4]
                    daycnt[i]["mail"] = daycnt[i]["mail"] + tl_port[i][j][5] + tl_port[i][j][6]
                    daycnt[i]["http"] = daycnt[i]["http"] + tl_port[i][j][7] + tl_port[i][j][8]
                    daycnt[i]["NetBIOS"] = daycnt[i]["NetBIOS"] + tl_port[i][j][9] + tl_port[i][j][10]
                    daycnt[i]["reflect"] = daycnt[i]["reflect"] + tl_port[i][j][11] + tl_port[i][j][12]
                    daycnt[i]["others"] = daycnt[i]["others"] + tl_port[i][j][13] + tl_port[i][j][14]
                elif (type == 4):  # src
                    daycnt[i]["ftp"] = daycnt[i]["ftp"] + tl_port[i][j][1]
                    daycnt[i]["ssh"] = daycnt[i]["ssh"] + tl_port[i][j][3]
                    daycnt[i]["mail"] = daycnt[i]["mail"] + tl_port[i][j][5]
                    daycnt[i]["http"] = daycnt[i]["http"] + tl_port[i][j][7]
                    daycnt[i]["NetBIOS"] = daycnt[i]["NetBIOS"] + tl_port[i][j][9]
                    daycnt[i]["reflect"] = daycnt[i]["reflect"] + tl_port[i][j][11]
                    daycnt[i]["others"] = daycnt[i]["others"] + tl_port[i][j][13]
                else:
                    daycnt[i]["ftp"] = daycnt[i]["ftp"] + tl_port[i][j][2]
                    daycnt[i]["ssh"] = daycnt[i]["ssh"] + tl_port[i][j][4]
                    daycnt[i]["mail"] = daycnt[i]["mail"] + tl_port[i][j][6]
                    daycnt[i]["http"] = daycnt[i]["http"] + tl_port[i][j][8]
                    daycnt[i]["NetBIOS"] = daycnt[i]["NetBIOS"] + tl_port[i][j][10]
                    daycnt[i]["reflect"] = daycnt[i]["reflect"] + tl_port[i][j][12]
                    daycnt[i]["others"] = daycnt[i]["others"] + tl_port[i][j][14]
    return daycnt

def calcu_tl_hour(day,type,tl_pro,tl_port):
    hourcnt=[]
    if(int(type/3)==0):
        #是protocal
        tmpdayarr=tl_pro[day]
        for i in range(len(tmpdayarr)):
            if(i%60==0):
                hourcnt.append({"tm": tmpdayarr[i][0], "tcp": 0, "udp": 0, "others": 0})
            tmpind=int(i/60)
            if (type == 0):  # all
                hourcnt[tmpind]["tcp"] = hourcnt[tmpind]["tcp"] + tmpdayarr[i][1] + tmpdayarr[i][2]
                hourcnt[tmpind]["udp"] = hourcnt[tmpind]["udp"] + tmpdayarr[i][3] + tmpdayarr[i][4]
                hourcnt[tmpind]["others"] = hourcnt[tmpind]["others"] + tmpdayarr[i][5] + tmpdayarr[i][6]
            elif (type == 1):  # src
                hourcnt[tmpind]["tcp"] = hourcnt[tmpind]["tcp"] + tmpdayarr[i][1]
                hourcnt[tmpind]["udp"] = hourcnt[tmpind]["udp"] + tmpdayarr[i][3]
                hourcnt[tmpind]["others"] = hourcnt[tmpind]["others"] + tmpdayarr[i][5]
            else:
                hourcnt[tmpind]["tcp"] = hourcnt[tmpind]["tcp"] + tmpdayarr[i][2]
                hourcnt[tmpind]["udp"] = hourcnt[tmpind]["udp"] + tmpdayarr[i][4]
                hourcnt[tmpind]["others"] = hourcnt[tmpind]["others"] + tmpdayarr[i][6]
    else:
        #是port
        tmpdayarr = tl_port[day]
        for i in range(len(tmpdayarr)):
            if (i % 60 == 0):
                hourcnt.append({"tm": tmpdayarr[i][0], "ftp": 0, "ssh": 0, "mail":0,"http":0,"NetBIOS":0,"reflect":0,"others": 0})
            tmpind = int(i / 60)
            if (type == 3):  # all
                hourcnt[tmpind]["ftp"] = hourcnt[tmpind]["ftp"] + tmpdayarr[i][1] + tmpdayarr[i][2]
                hourcnt[tmpind]["ssh"] = hourcnt[tmpind]["ssh"] + tmpdayarr[i][3] + tmpdayarr[i][4]
                hourcnt[tmpind]["mail"] = hourcnt[tmpind]["mail"] + tmpdayarr[i][5] + tmpdayarr[i][6]
                hourcnt[tmpind]["http"] = hourcnt[tmpind]["http"] + tmpdayarr[i][7] + tmpdayarr[i][8]
                hourcnt[tmpind]["NetBIOS"] = hourcnt[tmpind]["NetBIOS"] + tmpdayarr[i][9] + tmpdayarr[i][10]
                hourcnt[tmpind]["reflect"] = hourcnt[tmpind]["reflect"] + tmpdayarr[i][11] + tmpdayarr[i][12]
                hourcnt[tmpind]["others"] = hourcnt[tmpind]["others"] + tmpdayarr[i][13] + tmpdayarr[i][14]
            elif (type == 4):  # src
                hourcnt[tmpind]["ftp"] = hourcnt[tmpind]["ftp"] + tmpdayarr[i][1]
                hourcnt[tmpind]["ssh"] = hourcnt[tmpind]["ssh"] + tmpdayarr[i][3]
                hourcnt[tmpind]["mail"] = hourcnt[tmpind]["mail"] + tmpdayarr[i][5]
                hourcnt[tmpind]["http"] = hourcnt[tmpind]["http"] + tmpdayarr[i][7]
                hourcnt[tmpind]["NetBIOS"] = hourcnt[tmpind]["NetBIOS"] + tmpdayarr[i][9]
                hourcnt[tmpind]["reflect"] = hourcnt[tmpind]["reflect"] + tmpdayarr[i][11]
                hourcnt[tmpind]["others"] = hourcnt[tmpind]["others"] + tmpdayarr[i][13]
            else:
                hourcnt[tmpind]["ftp"] = hourcnt[tmpind]["ftp"] + tmpdayarr[i][2]
                hourcnt[tmpind]["ssh"] = hourcnt[tmpind]["ssh"] + tmpdayarr[i][4]
                hourcnt[tmpind]["mail"] = hourcnt[tmpind]["mail"] + tmpdayarr[i][6]
                hourcnt[tmpind]["http"] = hourcnt[tmpind]["http"] + tmpdayarr[i][8]
                hourcnt[tmpind]["NetBIOS"] = hourcnt[tmpind]["NetBIOS"] + tmpdayarr[i][10]
                hourcnt[tmpind]["reflect"] = hourcnt[tmpind]["reflect"] + tmpdayarr[i][12]
                hourcnt[tmpind]["others"] = hourcnt[tmpind]["others"] + tmpdayarr[i][14]
    return hourcnt

def calcu_tl_minu(day,hour,type,tl_pro,tl_port):
    minucnt=[]
    startline=hour*60
    endline=(hour+1)*60
    if(int(type/3)==0):
        #是protocal,
        tmpdayarr=np.array(tl_pro[day])
        tmphourarr=tmpdayarr[startline:endline,:]
        for i in range(len(tmphourarr)):
            minucnt.append({"tm": tmphourarr[i][0], "tcp": 0, "udp": 0, "others": 0})
            if (type == 0):  # all
                minucnt[i]["tcp"] = minucnt[i]["tcp"] + tmphourarr[i][1] + tmphourarr[i][2]
                minucnt[i]["udp"] = minucnt[i]["udp"] + tmphourarr[i][3] + tmphourarr[i][4]
                minucnt[i]["others"] = minucnt[i]["others"] + tmphourarr[i][5] + tmphourarr[i][6]
            elif (type == 1):  # src
                minucnt[i]["tcp"] = minucnt[i]["tcp"] + tmphourarr[i][1]
                minucnt[i]["udp"] = minucnt[i]["udp"] + tmphourarr[i][3]
                minucnt[i]["others"] = minucnt[i]["others"] + tmphourarr[i][5]
            else:
                minucnt[i]["tcp"] = minucnt[i]["tcp"] + tmphourarr[i][2]
                minucnt[i]["udp"] = minucnt[i]["udp"] + tmphourarr[i][4]
                minucnt[i]["others"] = minucnt[i]["others"] + tmphourarr[i][6]
    else:
        #是port
        tmpdayarr = tl_port[day]
        tmphourarr = tmpdayarr[startline:endline]
        for i in range(len(tmphourarr)):
            minucnt.append({"tm": tmphourarr[i][0], "ftp": 0, "ssh": 0, "mail":0,"http":0,"NetBIOS":0,"reflect":0,"others": 0})
            if (type == 3):  # all
                minucnt[i]["ftp"] = minucnt[i]["ftp"] + tmphourarr[i][1] + tmphourarr[i][2]
                minucnt[i]["ssh"] = minucnt[i]["ssh"] + tmphourarr[i][3] + tmphourarr[i][4]
                minucnt[i]["mail"] = minucnt[i]["mail"] + tmphourarr[i][5] + tmphourarr[i][6]
                minucnt[i]["http"] = minucnt[i]["http"] + tmphourarr[i][7] + tmphourarr[i][8]
                minucnt[i]["NetBIOS"] = minucnt[i]["NetBIOS"] + tmphourarr[i][9] + tmphourarr[i][10]
                minucnt[i]["reflect"] = minucnt[i]["reflect"] + tmphourarr[i][11] + tmphourarr[i][12]
                minucnt[i]["others"] = minucnt[i]["others"] + tmphourarr[i][13] + tmphourarr[i][14]
            elif (type == 4):  # src
                minucnt[i]["ftp"] = minucnt[i]["ftp"] + tmphourarr[i][1]
                minucnt[i]["ssh"] = minucnt[i]["ssh"] + tmphourarr[i][3]
                minucnt[i]["mail"] = minucnt[i]["mail"] + tmphourarr[i][5]
                minucnt[i]["http"] = minucnt[i]["http"] + tmphourarr[i][7]
                minucnt[i]["NetBIOS"] = minucnt[i]["NetBIOS"] + tmphourarr[i][9]
                minucnt[i]["reflect"] = minucnt[i]["reflect"] + tmphourarr[i][11]
                minucnt[i]["others"] = minucnt[i]["others"] + tmphourarr[i][13]
            else:
                minucnt[i]["ftp"] = minucnt[i]["ftp"] + tmphourarr[i][2]
                minucnt[i]["ssh"] = minucnt[i]["ssh"] + tmphourarr[i][4]
                minucnt[i]["mail"] = minucnt[i]["mail"] + tmphourarr[i][6]
                minucnt[i]["http"] = minucnt[i]["http"] + tmphourarr[i][8]
                minucnt[i]["NetBIOS"] = minucnt[i]["NetBIOS"] + tmphourarr[i][10]
                minucnt[i]["reflect"] = minucnt[i]["reflect"] + tmphourarr[i][12]
                minucnt[i]["others"] = minucnt[i]["others"] + tmphourarr[i][14]
    return minucnt


def cntdatabymin(newdata,begin,end):
    ftpsrc = 0
    ftpdst = 0
    sshsrc = 0
    sshdst = 0
    mailsrc = 0
    maildst = 0
    httpsrc = 0
    httpdst = 0
    netbiossrc = 0
    netbiosdst = 0
    reflectsrc = 0
    reflectdst = 0
    othersrc_port = 0
    otherdst_port = 0

    tcpsrc = 0
    tcpdst = 0
    udpsrc = 0
    udpdst = 0
    othersrc_pro = 0
    otherdst_pro = 0
    for line in newdata:
        srcport=line["firstSeenSrcPort"]
        dstport=line["firstSeenDestPort"]
        SrcTotalBytes=line["firstSeenSrcTotalBytes"]
        DestTotalBytes=line["firstSeenDestTotalBytes"]
        protocol=line["ipLayerProtocol"]
        #统计端口
        if (srcport == 20 or srcport == 21 or srcport == 115):
            ftpsrc = ftpsrc + int(SrcTotalBytes)
        elif (srcport == 22):
            sshsrc = sshsrc + int(SrcTotalBytes)
        elif (
                srcport == 25 or srcport == 109 or srcport == 110 or srcport == 143 or srcport == 465 or srcport == 993 or srcport == 995):
            mailsrc = mailsrc + int(SrcTotalBytes)
        elif (srcport == 80 or srcport == 443):
            httpsrc = httpsrc + int(SrcTotalBytes)
        elif (srcport == 137 or srcport == 138):
            netbiossrc = netbiossrc + int(SrcTotalBytes)
        elif (srcport == 53 or srcport == 123 or srcport == 1900 or srcport == 161 or srcport == 162 or srcport == 520):
            reflectsrc = reflectsrc + int(SrcTotalBytes)
        else:
            othersrc_port = othersrc_port + int(SrcTotalBytes)

        if (dstport == 20 or dstport == 21 or dstport == 115):
            ftpdst = ftpdst + int(DestTotalBytes)
        elif (dstport == 22):
            sshdst = sshdst + int(DestTotalBytes)
        elif (
                dstport == 25 or dstport == 109 or dstport == 110 or dstport == 143 or dstport == 465 or dstport == 993 or dstport == 995):
            maildst = maildst + int(DestTotalBytes)
        elif (dstport == 80 or dstport == 443):
            httpdst = httpdst + int(DestTotalBytes)
        elif (dstport == 137 or dstport == 138):
            netbiosdst = netbiosdst + int(DestTotalBytes)
        elif (dstport == 53 or dstport == 123 or dstport == 1900 or dstport == 161 or dstport == 162 or dstport == 520):
            reflectdst = reflectdst + int(DestTotalBytes)
        else:
            otherdst_port = otherdst_port + int(DestTotalBytes)

        #统计协议
        if (protocol == 6):
            tcpsrc = tcpsrc + int(SrcTotalBytes)
            tcpdst = tcpdst + int(DestTotalBytes)
        elif (protocol == 17):
            udpsrc = udpsrc + int(SrcTotalBytes)
            udpdst = udpdst + int(DestTotalBytes)
        else:
            othersrc_pro = othersrc_pro + int(SrcTotalBytes)
            otherdst_pro = otherdst_pro + int(DestTotalBytes)
    return [
        [begin, ftpsrc, ftpdst, sshsrc, sshdst, mailsrc, maildst, httpsrc, httpdst, netbiossrc, netbiosdst,
         reflectsrc, reflectdst, othersrc_port, otherdst_port],
        [begin, tcpsrc, tcpdst, udpsrc, udpdst, othersrc_pro, otherdst_pro]
    ]
