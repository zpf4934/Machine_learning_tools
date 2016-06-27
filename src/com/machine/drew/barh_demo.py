"""
Simple demo of a horizontal bar chart.
"""
import matplotlib.pyplot as plt
plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import sys

def dataset(filename,x,y,splittype):
    fr = open(filename)
    xdata = []
    ydata = {}
    if y != 'NONE':
        label = y.strip().split(',')
        for i in range(len(label)):
            if label[i].strip() is not None:
                ydata[float(label[i].strip())] = 0
        ydata[float("inf")] = 0
    for line in fr.readlines():
        data = line.strip().split(splittype)
        if y == 'NONE':
            if ydata.has_key(float(data[x-1])):
                ydata[float(data[x-1])] = ydata[float(data[x-1])] + 1
            else :
                ydata[float(data[x-1])] = 1
        else:
            i = 0
            label = y.strip().split(',')
            while i < len(label) and float(data[x-1]) > float(label[i].strip()):
                i = i + 1
            if i == len(label):
                ydata[float("inf")] = ydata[float("inf")] + 1
            else:
                ydata[float(label[i].strip())] = ydata[float(label[i].strip())] + 1     
    return ydata

# Example data
def drew(xdata,ydata):
    y_pos = np.arange(len(ydata))
    performance = np.array(ydata)
    error = [3]*len(xdata)

    
    plt.barh(y_pos, performance, xerr=error, align='center', alpha=0.4)
    plt.yticks(y_pos, xdata)
    plt.xlabel('Number')
    plt.ylabel('range')

    plt.show()

if __name__ == "__main__":
    if sys.argv[4] == "\\t":
        ydata = dataset(sys.argv[1],int(sys.argv[2]),sys.argv[3],"\t")
    else:
        ydata = dataset(sys.argv[1],int(sys.argv[2]),sys.argv[3],sys.argv[4])
    ylabel = []
    xlabel = ydata.keys()
    xlabel.sort()
    for i in range(len(xlabel)):
        ylabel.append(ydata[xlabel[i]])
    drew(xlabel,ylabel)
