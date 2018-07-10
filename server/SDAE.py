# coding: utf-8
from __future__ import division, print_function, absolute_import

import numpy as np
import sklearn.preprocessing as prep
import csv
import AE_para
import scipy

def standard_scale(X_train, X_test):
    preprocessor = prep.StandardScaler().fit(X_train)
    X_train = preprocessor.transform(X_train)
    X_test = preprocessor.transform(X_test)
    return X_train, X_test

# Load a CSV file
def loadCSV(filename):#加载数据，一行行的存入列表
    dataSet = []
    with open(filename, 'r') as file:
        csvReader = csv.reader(file)
        for line in csvReader:
            dataSet.append(line)
    return dataSet

# 除了标签列，其他列都转换为float类型
def column_to_float(dataSet):
    featLen = len(dataSet[0])
    for data in dataSet:
        for column in range(featLen):
            data[column] = float(data[column].strip())

def sigmoid(inputs):
    return [[1 / float(1 + scipy.special.expit(- x)) for x in input]  for input in inputs]


# 加载训练数据并shuffle
traindata = loadCSV('../client/data/nfminsum1-6.csv')
column_to_float(traindata)
traindata=np.array(traindata)
np.random.shuffle(traindata)

# 训练数据标准化
preprocessor0 = prep.StandardScaler().fit(traindata)
X_train = preprocessor0.transform(traindata)



X_train_0 = X_train

print("stack",0)
X_train_0 = sigmoid(np.dot(X_train_0, AE_para.SAE_w[0])+AE_para.SAE_b[0])
preprocessor1 = prep.StandardScaler().fit(X_train_0)
X_train_0 = preprocessor1.transform(X_train_0)

print("stack", 1)
X_train_0 = sigmoid(np.dot(X_train_0, AE_para.SAE_w[1])+AE_para.SAE_b[1])
preprocessor2 = prep.StandardScaler().fit(X_train_0)
X_train_0 = preprocessor2.transform(X_train_0)

print("stack", 2)
X_train_0 = sigmoid(np.dot(X_train_0, AE_para.SAE_w[2])+AE_para.SAE_b[2])
preprocessor3 = prep.StandardScaler().fit(X_train_0)
X_train_0 = preprocessor3.transform(X_train_0)

print("stack", 3)
X_train_0 = sigmoid(np.dot(X_train_0, AE_para.SAE_w[3])+AE_para.SAE_b[3])
preprocessor4 = prep.StandardScaler().fit(X_train_0)


preprocessor=[preprocessor1,preprocessor2,preprocessor3,preprocessor4]


def newdatafeature(newdata):
    for i in range(4):
        newdata = sigmoid(np.dot(newdata, AE_para.SAE_w[i]) + AE_para.SAE_b[i])
        newdata = preprocessor[i].transform(newdata)
    return newdata
