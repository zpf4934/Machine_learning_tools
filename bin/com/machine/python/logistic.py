# -*- coding: utf-8 -*-
'''
随机梯度上升使用方法：
1、trainstoc(filename,numIter,splittype)训练模型，filename训练数据，numIter控制迭代的次数，
2、prestoc(trainfile,prefile,outfile,numIter,splittype)数据预测，

梯度上升优化算法使用：
1、 pregrad(trainfile,prefile,outfile,numIter,splittype)numIter迭代次数
'''
from numpy import *
import sys

def sigmoid(inX):
    return 1.0/(1+exp(-inX))

def gradAscent(dataMatIn, numIter,classLabels):
    dataMatrix = mat(dataMatIn)            
    labelMat = mat(classLabels).transpose()
    m,n = shape(dataMatrix)
    alpha = 0.001
    maxCycles = numIter
    weights = ones((n,1))
    for k in range(maxCycles):              
        h = sigmoid(dataMatrix*weights)    
        error = (labelMat - h)             
        weights = weights + alpha * dataMatrix.transpose()* error 
    return weights

def stocGradAscent0(dataMatrix, classLabels):
    m,n = shape(dataMatrix)
    alpha = 0.01
    weights = ones(n)   
    for i in range(m):
        h = sigmoid(sum(dataMatrix[i]*weights))
        error = classLabels[i] - h
        weights = weights + alpha * error * dataMatrix[i]
    return weights

def stocGradAscent1(dataMatrix, classLabels, numIter=150):
    m,n = shape(dataMatrix)
    weights = ones(n)  
    for j in range(numIter):
        dataIndex = range(m)
        for i in range(m):
            alpha = 4/(1.0+j+i)+0.0001    
            randIndex = int(random.uniform(0,len(dataIndex)))
            h = sigmoid(sum(dataMatrix[randIndex]*weights))
            error = classLabels[randIndex] - h
            weights = weights + alpha * error * dataMatrix[randIndex]
            del(dataIndex[randIndex])
    return weights

def classifyVector(inX, weights):
    prob = sigmoid(sum(inX*weights))
    if prob > 0.5: return 1.0
    else: return 0.0

def colicTest(filename,numIter,splittype):
    frTrain = open(filename); frTest = open(filename)
    trainingSet = []; trainingLabels = []
    for line in frTrain.readlines():
        currLine = line.strip().split(splittype)
        lineArr =[]
        n = len(currLine)
        for i in range(n-1):
            lineArr.append(float(currLine[i]))
        trainingSet.append(lineArr)
        trainingLabels.append(float(currLine[-1]))
    trainWeights = stocGradAscent1(array(trainingSet), trainingLabels, numIter)
    errorCount = 0; numTestVec = 0.0
    for line in frTest.readlines():
        numTestVec += 1.0
        currLine = line.strip().split(splittype)
        lineArr =[]
        for i in range(n-1):
            lineArr.append(float(currLine[i]))
        if float(classifyVector(array(lineArr), trainWeights))!= float(currLine[-1]):
            errorCount += 1
    errorRate = (float(errorCount)/numTestVec)
    print "the error rate of this test is: %f" % errorRate
    return errorRate

def colicTestgrad(filename,numIter,splittype):
    frTrain = open(filename); frTest = open(filename)
    trainingSet = []; trainingLabels = []
    for line in frTrain.readlines():
        currLine = line.strip().split(splittype)
        lineArr =[]
        n = len(currLine)
        for i in range(n-1):
            lineArr.append(float(currLine[i]))
        trainingSet.append(lineArr)
        trainingLabels.append(float(currLine[-1]))
    trainWeights = gradAscent(array(trainingSet),numIter,trainingLabels)
    errorCount = 0; numTestVec = 0.0
    for line in frTest.readlines():
        numTestVec += 1.0
        currLine = line.strip().split(splittype)
        lineArr =[]
        for i in range(n-1):
            lineArr.append(float(currLine[i]))
        if float(classifyVector(array(lineArr), trainWeights))!= float(currLine[-1]):
            errorCount += 1
    errorRate = (float(errorCount)/numTestVec)
    print "the error rate of this test is: %f" % errorRate
    return errorRate

def colicTeststoc(filename,splittype):
    frTrain = open(filename); frTest = open(filename)
    trainingSet = []; trainingLabels = []
    for line in frTrain.readlines():
        currLine = line.strip().split(splittype)
        lineArr =[]
        n = len(currLine)
        for i in range(n-1):
            lineArr.append(float(currLine[i]))
        trainingSet.append(lineArr)
        trainingLabels.append(float(currLine[-1]))
    trainWeights = stocGradAscent0(array(trainingSet), trainingLabels)
    errorCount = 0; numTestVec = 0.0
    for line in frTest.readlines():
        numTestVec += 1.0
        currLine = line.strip().split(splittype)
        lineArr =[]
        for i in range(n-1):
            lineArr.append(float(currLine[i]))
        if float(classifyVector(array(lineArr), trainWeights))!= float(currLine[-1]):
            errorCount += 1
    errorRate = (float(errorCount)/numTestVec)
    print "the error rate of this test is: %f" % errorRate
    return errorRate

def colicpre(trainfile,prefile,outfile,numIter,splittype):
    frTrain = open(trainfile); frTest = open(prefile)
    fw = open(outfile,'a')
    trainingSet = []; trainingLabels = []
    for line in frTrain.readlines():
        currLine = line.strip().split(splittype)
        lineArr =[]
        n = len(currLine)
        for i in range(n-1):
            lineArr.append(float(currLine[i]))
        trainingSet.append(lineArr)
        trainingLabels.append(float(currLine[-1]))
    trainWeights = stocGradAscent1(array(trainingSet), trainingLabels, numIter)
    errorCount = 0; numTestVec = 0.0
    for line in frTest.readlines():
        numTestVec += 1.0
        currLine = line.strip().split(splittype)
        n = len(currLine)
        lineArr =[]
        for i in range(n):
            lineArr.append(float(currLine[i]))
        classlabel = classifyVector(array(lineArr), trainWeights)
        for i in range(len(lineArr)):
            fw.write(str(lineArr[i]) + splittype)
        fw.write(str(classlabel) + '\n')
        fw.flush()
        
def gradpre(trainfile,prefile,outfile,numIter,splittype):
    frTrain = open(trainfile); frTest = open(prefile)
    fw = open(outfile,'a')
    trainingSet = []; trainingLabels = []
    for line in frTrain.readlines():
        currLine = line.strip().split(splittype)
        lineArr =[]
        n = len(currLine)
        for i in range(n-1):
            lineArr.append(float(currLine[i]))
        trainingSet.append(lineArr)
        trainingLabels.append(float(currLine[-1]))
    trainWeights = gradAscent(array(trainingSet), numIter,trainingLabels)
    errorCount = 0; numTestVec = 0.0
    for line in frTest.readlines():
        numTestVec += 1.0
        currLine = line.strip().split(splittype)
        n = len(currLine)
        lineArr =[]
        for i in range(n):
            lineArr.append(float(currLine[i]))
        classlabel = classifyVector(array(lineArr), trainWeights)
        for i in range(len(lineArr)):
            fw.write(str(lineArr[i]) + splittype)
        fw.write(str(classlabel) + '\n')
        fw.flush()

def stocpre(trainfile,prefile,outfile,splittype):
    frTrain = open(trainfile); frTest = open(prefile)
    fw = open(outfile,'a')
    trainingSet = []; trainingLabels = []
    for line in frTrain.readlines():
        currLine = line.strip().split(splittype)
        lineArr =[]
        n = len(currLine)
        for i in range(n-1):
            lineArr.append(float(currLine[i]))
        trainingSet.append(lineArr)
        trainingLabels.append(float(currLine[-1]))
    trainWeights = stocGradAscent0(array(trainingSet), trainingLabels)
    errorCount = 0; numTestVec = 0.0
    for line in frTest.readlines():
        numTestVec += 1.0
        currLine = line.strip().split(splittype)
        n = len(currLine)
        lineArr =[]
        for i in range(n):
            lineArr.append(float(currLine[i]))
        classlabel = classifyVector(array(lineArr), trainWeights)
        for i in range(len(lineArr)):
            fw.write(str(lineArr[i]) + splittype)
        fw.write(str(classlabel) + '\n')
        fw.flush()
        
def multiTest(filename,numIter,splittype):
    numTests = 10; errorSum=0.0
    for k in range(numTests):
        errorSum += colicTest(filename,numIter,splittype)
    print "after %d iterations the average error rate is: %f" % (numTests, errorSum/float(numTests))

def multiTestgrad(filename,numIter,splittype):
    numTests = 10; errorSum=0.0
    for k in range(numTests):
        errorSum += colicTestgrad(filename,numIter,splittype)
    print "after %d iterations the average error rate is: %f" % (numTests, errorSum/float(numTests))

def multiTeststoc(filename,splittype):
    numTests = 10; errorSum=0.0
    for k in range(numTests):
        errorSum += colicTeststoc(filename,splittype)
    print "after %d iterations the average error rate is: %f" % (numTests, errorSum/float(numTests))

def trainstoc_beater(filename,numIter,splittype):
    print "running...."
    multiTest(filename,numIter,splittype)
    print "end...."

def prestoc_beater(trainfile,prefile,outfile,numIter,splittype):
    print "running...."
    colicpre(trainfile,prefile,outfile,numIter,splittype)
    print "end...."

def traingrad(filename,numIter,splittype):
    print "running...."
    multiTestgrad(filename,numIter,splittype)
    print "end...."

def pregrad(trainfile,prefile,outfile,numIter,splittype):
    print "running...."
    gradpre(trainfile,prefile,outfile,numIter,splittype)
    print "end...."

def trainstoc(filename,splittype):
    print "running...."
    multiTeststoc(filename,splittype) 
    print "end...."

def prestoc(trainfile,prefile,outfile,splittype):
    print "running...."
    stocpre(trainfile,prefile,outfile,splittype)
    print "end...."

if __name__ == "__main__":
	if len(sys.argv) == 5 and sys.argv[1] == "stoc":
		if sys.argv[4] == "\\t":
			trainstoc_beater(sys.argv[2],int(sys.argv[3]),"\t")
		else:
			trainstoc_beater(sys.argv[2],int(sys.argv[3]),sys.argv[4])
	elif len(sys.argv) == 7 and sys.argv[1] == "stoc":
		if sys.argv[6] == "\\t":
			prestoc_beater(sys.argv[2],sys.argv[3],sys.argv[4],int(sys.argv[5]),"\t")
		else:
			prestoc_beater(sys.argv[2],sys.argv[3],sys.argv[4],int(sys.argv[5]),sys.argv[6])
	elif len(sys.argv) == 5 and sys.argv[1] == "grad":
		if sys.argv[4] == "\\t":
			traingrad(sys.argv[2],int(sys.argv[3]),"\t")
		else:
			traingrad(sys.argv[2],int(sys.argv[3]),sys.argv[4])
	elif len(sys.argv) == 7 and sys.argv[1] == "grad":
		if sys.argv[6] == "\\t":
			pregrad(sys.argv[2],sys.argv[3],sys.argv[4],int(sys.argv[5]),"\t")
		else:
			pregrad(sys.argv[2],sys.argv[3],sys.argv[4],int(sys.argv[5]),sys.argv[6])
	elif len(sys.argv) == 4 and sys.argv[1] == "toc":
		if sys.argv[3] == "\\t":
			trainstoc(sys.argv[2],"\t")
		else:
			trainstoc(sys.argv[2],sys.argv[3])
	elif len(sys.argv) == 6 and sys.argv[1] == "toc":
		if sys.argv[5] == "\\t":
			prestoc(sys.argv[2],sys.argv[3],sys.argv[4],"\t")	
		else:		
			prestoc(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
