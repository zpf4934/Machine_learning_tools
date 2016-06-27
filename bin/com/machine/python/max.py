
from numpy import *
import sys

def loadset(filename,n,splittype):
    fr = open(filename)
    datamat = []
    i = int(n)
    maxs = float("-inf")
    for line in fr.readlines():
        lines = line.strip().split(splittype)
        if maxs < float(lines[i-1]):
            maxs = float(lines[i-1])
    return maxs

def test(filename,n,splittype):
    maxs = loadset(filename,n,splittype)
    print 'max is : ' + str(maxs)

if __name__ == "__main__":
	if sys.argv[3] == "\\t":
		test(sys.argv[1],int(sys.argv[2]),"\t")
	else:
		test(sys.argv[1],int(sys.argv[2]),sys.argv[3])
