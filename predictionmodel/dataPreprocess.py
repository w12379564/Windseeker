import numpy as np
from predictionmodel.models import weathertest

def file2dataset(filename,size,shuffleornot):
    f = open(filename, 'r')
    line = f.readline()
    count = 0
    temp = []
    hum = []
    press = []
    wd = []
    rawdata = []
    while line:
        l = line.split(' ')
        temp.append(float(l[1]))
        hum.append(float(l[2]))
        press.append(float(l[3]))
        wd.append(float(l[5]) / 3.6)
        count = count + 1
        if count == size:
            rawdata.append(wd + temp + hum + press)
            temp = []
            hum = []
            press = []
            wd = []
            count = 0
        line = f.readline()

    data = np.array(rawdata)
    if shuffleornot==1: np.random.shuffle(data)
    return data

def db2dataset(size,begtime,endtime):
    count = 0
    temp = []
    hum = []
    press = []
    wd = []
    rawdata = []
    for record in weathertest.objects.filter(time__gte = begtime).filter(time__lte = endtime):
        temp.append(record.temp)
        hum.append(record.hum)
        press.append(record.press)
        wd.append(record.windspeed/3.6)
        count = count + 1
        if count == size:
            rawdata.append(wd + temp + hum + press)
            temp = []
            hum = []
            press = []
            wd = []
            count = 0

    data = np.array(rawdata)
    return data