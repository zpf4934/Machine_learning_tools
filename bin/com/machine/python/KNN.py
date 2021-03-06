# -*- coding: utf-8 -*-
'''
use method
1、test(trainfile,k,splittype)trainfile代表训练数据，k代表距离预测点最近的点的个数，splittype代表数据切分表示符
2、pre(trainfile,testfile,outfile,k,splittype)trainfile代表训练数据，testfile代表预测数据，outfile代表输出文件，k代表距离预测值最近的点的个数，splittype代表数据分割标示符
'''
from numpy import *
import operator
from os import listdir
import sys

def classify0(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    diffMat = tile(inX, (dataSetSize,1)) - dataSet
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances**0.5
    sortedDistIndicies = distances.argsort()     
    classCount={}          
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

def file2matrix(filename,splittype):
    fr = open(filename)
    n = len(fr.readline().split(splittype)) - 1
    fr.close()
    fr = open(filename)
    numberOfLines = len(fr.readlines())
    returnMat = zeros((numberOfLines,n))       
    classLabelVector = []
    fr.close()
    fr = open(filename)
    index = 0
    for line in fr.readlines():
        line = line.strip()
        listFromLine = line.split(splittype)
        returnMat[index,:] = listFromLine[0:n]
        classLabelVector.append(listFromLine[-1])
        index += 1
    fr.close()
    return returnMat,classLabelVector

def file1matrix(filename,splittype):
    fr = open(filename)
    n = len(fr.readline().split(splittype))
    fr.close()
    fr = open(filename)
    numberOfLines = len(fr.readlines())
    returnMat = zeros((numberOfLines,n))
    fr.close()
    fr = open(filename)
    index = 0
    for line in fr.readlines():
        line = line.strip()
        listFromLine = line.split(splittype)
        returnMat[index,:] = listFromLine[0:n]
        index += 1
    fr.close()
    return returnMat
    
def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataSet = zeros(shape(dataSet))
    m = dataSet.shape[0]
    normDataSet = dataSet - tile(minVals, (m,1))
    normDataSet = normDataSet/tile(ranges, (m,1))   
    return normDataSet, ranges, minVals
   
def datingClassTest(filename,k,splittype):
    hoRatio = 0.10      #测试数据比例
    datingDataMat,datingLabels = file2matrix(filename,splittype)      
    normMat, ranges, minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]
    numTestVecs = int(m*hoRatio)
    errorCount = 0.0
    for i in range(numTestVecs):
        classifierResult = classify0(normMat[i,:],normMat[numTestVecs:m,:],datingLabels[numTestVecs:m],k)
        print "the classifier came back with: %s, the real answer is: %s" % (classifierResult, datingLabels[i])
        if (classifierResult != datingLabels[i]): errorCount += 1.0
    print "the total error rate is: %f" % (errorCount/float(numTestVecs))
    print errorCount

def datingClasspre(trainfile,testfile,outfile,k,splittype):
    datingDataMat,datingLabels = file2matrix(trainfile,splittype)      
    normMat, ranges, minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]
    numTestVecs = file1matrix(testfile,splittype)
    Testdata,rangess,minVal = autoNorm(numTestVecs)
    fw = open(outfile,'a')
    for i in range(len(numTestVecs)):
        classifierResult = classify0(Testdata[i],normMat,datingLabels,k)
        print "the classifier came back with: %s" % (classifierResult)
        for n in range(len(numTestVecs[i])):
            fw.write(str(numTestVecs[i][n]).strip() + splittype)
        fw.write(classifierResult + '\n')
        fw.flush()
    fw.close()

def test(filename,k,splittype):
    print "running...."
    datingClassTest(filename,k,splittype)
    print "end...."

def pre(trainfile,testfile,outfile,k,splittype):
    print "running...."
    datingClasspre(trainfile,testfile,outfile,k,splittype)
    print "end...."

if __name__ == "__main__":
	if len(sys.argv) == 4:
		if sys.argv[3] == "\\t":
			test(sys.argv[1],int(sys.argv[2]),"\t")
		else:
			test(sys.argv[1],int(sys.argv[2]),sys.argv[3])
	elif len(sys.argv) == 6:
		if sys.argv[5] == "\\t":
			pre(sys.argv[1],sys.argv[2],sys.argv[3],int(sys.argv[4]),"\t")
		else:
			pre(sys.argv[1],sys.argv[2],sys.argv[3],int(sys.argv[4]),sys.argv[5])
