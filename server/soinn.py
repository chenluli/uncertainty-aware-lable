#! /usr/bin/python
# -*- coding:utf-8 -*-
import numpy as np
from numpy import linalg as LA


def initSOINN(p_data, p_agemax, p_lambda, p_c, finnal_denoise):
    #feature_num=p_data[0].shape[0]
    data_num=len(p_data)
    node=[p_data[0],p_data[1]]

    M=[1,1]
    tem=LA.norm(p_data[0]-p_data[-1])
    threshold = [tem, tem]
    connection = np.array([[0, 0],[0, 0]])
    age = np.array([[0, 0],[0, 0]])

    for i in xrange(2,data_num):
        # find winner node and runner-up node
        minval=1000000
        minval2=1000000
        minind=-1
        minind2=-1
        #找出与p_data[i]最相似的两个神经元
        for j in xrange(len(node)):
            dis = LA.norm(p_data[i]-node[j])
            if dis<minval:
                minval2 = minval
                minind2 = minind
                minval=dis
                minind=j
            elif dis<minval2:
                minval2=dis
                minind2=j
        # prototype, connection and age update
        #如果大于阈值，生成一个新的节点
        if minval==0:continue
        if minval>threshold[minind] or minval2>threshold[minind2]:
            node.append(p_data[i])
            threshold.append(minval2+minval)
            M.append(1)
            #node_time.append([[p_data_time[i],p_data_time[i]+60]])
            connection=np.row_stack((connection,np.zeros(connection.shape[1])))
            connection=np.column_stack((connection,np.zeros(connection.shape[0])))
            age = np.row_stack((age, np.zeros(age.shape[1])))
            age = np.column_stack((age, np.zeros(age.shape[0])))
        else:
            # 如果S1与S2间不存在连接，为两个最相似节点建立连接

            #if connection[minind][minind2]==0:
            #    connection[minind][minind2]=1
            #    connection[minind2][minind]=1

            connection[minind][minind2] = connection[minind][minind2]+1
            connection[minind2][minind] = connection[minind2][minind]+1
            #刷新边(sl，s2)的年龄参数
            age[minind][minind2] = 1
            age[minind2][minind] = 1

            #与胜者节点相连的所有边age参数加1
            col=np.where(connection[minind,:]!=0)[0]
            for j in xrange(len(col)):
                age[minind][col[j]]=age[minind][col[j]]+1
                age[col[j]][minind] = age[col[j]][minind] + 1
            #检查所有连接,如果>p_agemax,就移除该连接．
            locate=np.where(age[minind]>p_agemax)[0]
            for j in range(len(locate)):
                connection[minind][locate[j]]=0
                connection[locate[j]][minind]=0
                age[minind][locate[j]]=0
                age[locate[j]][minind] = 0
            M[minind]=M[minind]+1
            #更新两个胜者节点的权值
            node[minind]=node[minind]+(1/float(M[minind]))*(p_data[i]-node[minind])
            node[minind2]=node[minind2]+(0.01/float(M[minind2]))*(p_data[i]-node[minind2])

        # threshold update
        nnz=len(np.where(connection[minind] != 0)[0])
        if nnz==0:
            threshold[minind]=LA.norm(node[minind]-node[minind2])
        else:
            v1=np.where(connection[minind] != 0)[0]
            maxdis1=0
            for j in xrange(len(v1)):
                distance=LA.norm(node[minind]-node[v1[j]])
                if distance>maxdis1:
                    maxdis1=distance
            threshold[minind]=maxdis1

        nnz2 = len(np.where(connection[minind2] != 0)[0])
        if nnz2 == 0:
            threshold[minind2] = LA.norm(node[minind] - node[minind2])
        else:
            v2 = np.where(connection[minind2] != 0)[0]
            maxdis2 = 0
            for j in xrange(len(v2)):
                distance = LA.norm(node[minind2] - node[v2[j]])
                if distance > maxdis2:
                    maxdis2 = distance
            threshold[minind2] = maxdis2
        # denosing
        if (i+1)%p_lambda==0 or (finnal_denoise and i==data_num-1):
            meanM=float(np.sum(np.array(M)))/len(M)
            connection2=np.where(connection > 0, 1, 0)
            neighbor=np.sum(connection2, axis=0)
            #如果一个节点没有邻居节点 或者只有一个邻居节点，而且成为胜者的次数低于当前神经元的平均次数一定比例
            setu=np.union1d(np.intersect1d(np.where(np.array(M)<p_c*meanM)[0],np.where(neighbor==1)[0]),np.intersect1d(np.where(np.array(M)<meanM)[0],np.where(neighbor==0)[0]))
            #setu.sort()
            for j in xrange(len(setu)):
                tmp=len(setu)-j-1
                del threshold[setu[tmp]]
                del M[setu[tmp]]
                del node[setu[tmp]]
            connection=np.delete(connection, setu, axis=0)
            connection=np.delete(connection, setu, axis=1)
            age=np.delete(age, setu, axis=0)
            age=np.delete(age, setu, axis=1)
            #print "j"
        #print threshold
    return node,connection,M,threshold,age



def connect2json(features,features_TSNE,connection,age,wincnt,threshold):
    nodes=[]
    links=[]
    for i in range(len(connection)):
        nodes.append({"id":i,"wincnt":wincnt[i],"features_all":features[i].tolist(),"feature":features_TSNE[i].tolist(),"threshold":threshold[i],"type":"uncertain","certainty":[0,0,1],"labeled":0})
    for i in range(len(connection)):
        for j in range(i,len(connection)):
            if(connection[i][j]>0):
                links.append({"source":i,"target":j,"cnt":connection[i][j],"age":age[i][j]})
    return nodes,links


def calcu_dis(nodes):
    nodesnum=nodes.shape[0]
    dis=np.zeros((nodesnum,nodesnum))
    for i in range(nodesnum):
        for j in range(i+1,nodesnum):
            dis[i][j] = LA.norm(nodes[i] - nodes[j])
            dis[j][i]=dis[i][j]
    return dis

def matchdata(data,node,threshold):
    timematcharr=[]
    for i in xrange(len(data)):
        # find winner node and runner-up node
        minval=1000000
        minval2=1000000
        minind=-1
        minind2=-1
        #找出最相似的两个神经元
        for j in xrange(len(node)):
            dis = LA.norm(data[i]-node[j])
            if dis<minval:
                minval2 = minval
                minind2 = minind
                minval=dis
                minind=j
            elif dis<minval2:
                minval2=dis
                minind2=j
        if minval <= threshold[minind] and minval2 > threshold[minind2]:
            timematcharr.append(["uncertain_"+str(minind)])
        elif minval > threshold[minind] and minval2 <= threshold[minind2]:
            timematcharr.append(["uncertain_"+str(minind2)])
        elif minval > threshold[minind] and minval2 > threshold[minind2]:
            timematcharr.append([-1])
        else:
            timematcharr.append(["uncertain_"+str(minind),"uncertain_"+str(minind2)])
    return timematcharr

def matchdata2(p_data,node,connection,wincnt,threshold,age, p_agemax):
    data_num=len(p_data)
    timematcharr = []

    for i in range(len(wincnt)):
        wincnt[i] = 1
        for j in range(len(wincnt)):
            age[i][j] = 0
            connection[i][j] = 0

    for i in xrange(data_num):
        # find winner node and runner-up node
        minval=1000000
        minval2=1000000
        minind=-1
        minind2=-1
        #找出与p_data[i]最相似的两个神经元
        for j in xrange(len(node)):
            dis = LA.norm(p_data[i]-node[j])
            if dis<minval:
                minval2 = minval
                minind2 = minind
                minval=dis
                minind=j
            elif dis<minval2:
                minval2=dis
                minind2=j
        # prototype, connection and age update

        if minval <= threshold[minind] and minval2 > threshold[minind2]:
            timematcharr.append(["uncertain_"+str(minind)])
            wincnt[minind] = wincnt[minind] + 1
        elif minval > threshold[minind] and minval2 <= threshold[minind2]:
            timematcharr.append(["uncertain_"+str(minind2)])
            wincnt[minind2] = wincnt[minind2] + 1
        elif minval > threshold[minind] and minval2 > threshold[minind2]:
            timematcharr.append(["uncertain_" + str(minind)])
            threshold[minind] = LA.norm(node[minind] - p_data[i])
            wincnt[minind] = wincnt[minind] + 1
            '''
            #如果大于阈值，生成一个新的节点
            timematcharr.append(["uncertain_" + str(len(node))])
            node.append(p_data[i])
            threshold.append(minval2+minval)
            wincnt.append(1)
            connection=np.row_stack((connection,np.zeros(connection.shape[1])))
            connection=np.column_stack((connection,np.zeros(connection.shape[0])))
            age = np.row_stack((age, np.zeros(age.shape[1])))
            age = np.column_stack((age, np.zeros(age.shape[0])))
            '''

        else:
            timematcharr.append(["uncertain_" + str(minind), "uncertain_" + str(minind2)])
            # 如果S1与S2间不存在连接，为两个最相似节点建立连接
            connection[minind][minind2] = connection[minind][minind2]+1
            connection[minind2][minind] = connection[minind2][minind]+1
            #刷新边(sl，s2)的年龄参数
            age[minind][minind2] = 1
            age[minind2][minind] = 1
            #与胜者节点相连的所有边age参数加1
            col=np.where(connection[minind,:]!=0)[0]
            for j in xrange(len(col)):
                age[minind][col[j]]=age[minind][col[j]]+1
                age[col[j]][minind] = age[col[j]][minind] + 1
            #检查所有连接,如果>p_agemax,就移除该连接．
            locate=np.where(age[minind]>p_agemax)[0]
            for j in range(len(locate)):
                connection[minind][locate[j]]=0
                connection[locate[j]][minind]=0
                age[minind][locate[j]]=0
                age[locate[j]][minind] = 0
            wincnt[minind]=wincnt[minind]+1


    return timematcharr,node,connection,wincnt,threshold,age

def SOINN_addnode(newfeat,node,connection,wincnt,threshold,age):
    # 找出与newfeat最相似的两个神经元
    minval = 1000000
    minval2 = 1000000
    minind = -1
    minind2 = -1
    for j in xrange(len(node)):
        dis = LA.norm(newfeat - node[j])
        if dis < minval:
            minval2 = minval
            minind2 = minind
            minval = dis
            minind = j
        elif dis < minval2:
            minval2 = dis
            minind2 = j

    # 增加节点
    node.append(newfeat)
    threshold.append(minval2 + minval)
    wincnt.append(1)
    connection = np.row_stack((connection, np.zeros(connection.shape[1])))
    connection = np.column_stack((connection, np.zeros(connection.shape[0])))
    age = np.row_stack((age, np.zeros(age.shape[1])))
    age = np.column_stack((age, np.zeros(age.shape[0])))

    #新增加的节点与两个胜者节点连接
    newind=len(node)-1
    connection[minind][newind] = 1
    connection[newind][minind] = 1
    connection[minind2][newind] = 1
    connection[newind][minind2] = 1

    # 反向更新两个胜者节点的权值
    node[minind] = node[minind] - (1 / float(wincnt[minind])) * (newfeat - node[minind])
    node[minind2] = node[minind2] - (0.01 / float(wincnt[minind2])) * (newfeat - node[minind2])

    # 更新两个胜者节点的阈值
    nnz = len(np.where(connection[minind] != 0)[0])
    if nnz == 0:
        threshold[minind] = LA.norm(node[minind] - node[minind2])
    else:
        v1 = np.where(connection[minind] != 0)[0]
        maxdis1 = 0
        for j in xrange(len(v1)):
            distance = LA.norm(node[minind] - node[v1[j]])
            if distance > maxdis1:
                maxdis1 = distance
        threshold[minind] = maxdis1
    nnz2 = len(np.where(connection[minind2] != 0)[0])
    if nnz2 == 0:
        threshold[minind2] = LA.norm(node[minind] - node[minind2])
    else:
        v2 = np.where(connection[minind2] != 0)[0]
        maxdis2 = 0
        for j in xrange(len(v2)):
            distance = LA.norm(node[minind2] - node[v2[j]])
            if distance > maxdis2:
                maxdis2 = distance
        threshold[minind2] = maxdis2

    if connection[minind][minind2] >0:
        connection[minind][minind2] =0
        connection[minind2][minind] =0
    return node, connection, wincnt, threshold, age,minind,minind2


