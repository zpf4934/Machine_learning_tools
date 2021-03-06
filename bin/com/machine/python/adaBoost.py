# -*- coding: utf-8 -*-
'''
使用方法：
首先使用train(filename,numiter,splittype)进行模型的训练进行错误率计算，选择适合的模型。filename是训练数据，numiter是用户指定的函数迭代次数，splittype是数据分割表示符
得出最好的训练模型之后就可以调用pre(trainfile,prefile,outfile,numiter,splittype)进行预测，
'''
from numpy import *
import sys


def loadDataSet(fileName,splittype):     
    numFeat = len(open(fileName).readline().split(splittype))
    dataMat = []; labelMat = []
    fr = open(fileName)
    for line in fr.readlines():
        lineArr =[]
        curLine = line.strip().split(splittype)
        for i in range(numFeat-1):
            lineArr.append(float(curLine[i]))
        dataMat.append(lineArr)
        labelMat.append(float(curLine[-1]))
    return dataMat,labelMat

def stumpClassify(dataMatrix,dimen,threshVal,threshIneq):
    retArray = ones((shape(dataMatrix)[0],1))
    if threshIneq == 'lt':
        retArray[dataMatrix[:,dimen] <= threshVal] = -1.0
    else:
        retArray[dataMatrix[:,dimen] > threshVal] = -1.0
    return retArray
    

def buildStump(dataArr,classLabels,D):
    dataMatrix = mat(dataArr); labelMat = mat(classLabels).T
    m,n = shape(dataMatrix)
    numSteps = 10.0; bestStump = {}; bestClasEst = mat(zeros((m,1)))
    minError = inf 
    for i in range(n):
        rangeMin = dataMatrix[:,i].min(); rangeMax = dataMatrix[:,i].max();
        stepSize = (rangeMax-rangeMin)/numSteps
        for j in range(-1,int(numSteps)+1):
            for inequal in ['lt', 'gt']:
                threshVal = (rangeMin + float(j) * stepSize)
                predictedVals = stumpClassify(dataMatrix,i,threshVal,inequal)
                errArr = mat(ones((m,1)))
                errArr[predictedVals == labelMat] = 0
                weightedError = D.T*errArr 
                if weightedError < minError:
                    minError = weightedError
                    bestClasEst = predictedVals.copy()
                    bestStump['dim'] = i
                    bestStump['thresh'] = threshVal
                    bestStump['ineq'] = inequal
    return bestStump,minError,bestClasEst


def adaBoostTrainDS(dataArr,classLabels,numIt=40):
    weakClassArr = []
    m = shape(dataArr)[0]
    D = mat(ones((m,1))/m)   
    aggClassEst = mat(zeros((m,1)))
    for i in range(numIt):
        bestStump,error,classEst = buildStump(dataArr,classLabels,D)
        alpha = float(0.5*log((1.0-error)/max(error,1e-16)))
        bestStump['alpha'] = alpha  
        weakClassArr.append(bestStump)                 
        expon = multiply(-1*alpha*mat(classLabels).T,classEst) 
        D = multiply(D,exp(expon))                            
        D = D/D.sum()
        aggClassEst += alpha*classEst
        aggErrors = multiply(sign(aggClassEst) != mat(classLabels).T,ones((m,1)))
        errorRate = aggErrors.sum()/m
        print "total error: ",errorRate
        if errorRate == 0.0: break
    return weakClassArr

def adaClassify(datToClass,classifierArr):
    dataMatrix = mat(datToClass)
    m = shape(dataMatrix)[0]
    aggClassEst = mat(zeros((m,1)))
    for i in range(len(classifierArr)):
        classEst = stumpClassify(dataMatrix,classifierArr[i]['dim'],\
                                 classifierArr[i]['thresh'],\
                                 classifierArr[i]['ineq'])
        aggClassEst += classifierArr[i]['alpha']*classEst
    return sign(aggClassEst)

def train(filename,numiter,splittype):
    print "running...."
    data,label = loadDataSet(filename,splittype)
    classfi = adaBoostTrainDS(data,label,numiter)
    pred = adaClassify(data,classfi)
    errArr = mat(ones((len(data),1)))
    print errArr[pred != mat(label).T].sum()/len(data)
    print "end...."

def pre(trainfile,prefile,outfile,numiter,splittype):
    print "running...."
    data,label = loadDataSet(trainfile,splittype)
    classfi = adaBoostTrainDS(data,label,numiter)
    datas = []
    fr = open(prefile)
    fw = open(outfile,'a')
    for line in fr.readlines():
        data = line.strip().split(splittype)
        datas.append(data)
    pre = adaClassify(datas,classfi)
    fr.close()
    fr = open(prefile)
    i = 0
    pred = pre.tolist()
    for line in fr.readlines():
        fw.write(line.strip() + '\t' + str(pred[i][0]) + '\n')
        i += 1
    fw.flush()
    fw.close()
    print "end...."

if __name__ == "__main__":
	if len(sys.argv) == 6:
		if sys.argv[5] == "\\t":
			pre(sys.argv[1],sys.argv[2],sys.argv[3],int(sys.argv[4]),"\t")
		else:
			pre(sys.argv[1],sys.argv[2],sys.argv[3],int(sys.argv[4]),sys.argv[5])
	elif len(sys.argv) == 4:
		if sys.argv[3] == "\\t":
			train(sys.argv[1],int(sys.argv[2]),"\t")
		else:	
			train(sys.argv[1],int(sys.argv[2]),sys.argv[3])
