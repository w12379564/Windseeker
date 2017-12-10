import numpy as np
from predictionmodel.models import weathertest
from predictionmodel.models import HistoryData
from django.db.models import Sum
from datetime import datetime,timedelta
from predictionmodel.models import HistoryData
from django.db.models import Sum,Max

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

def Db2ShortTermData(begtime,endtime):
    #history = HistoryData.objects.filter(time__gte = begtime).filter(time__lt = endtime).values_list('time').annotate(Power_Sum=Sum('power')).values_list('Power_Sum',flat=True)
    dataset = {'x_train':[],'y_train':[]}
    nowtime = endtime
    while nowtime > begtime:
        x_end = nowtime
        x_begin = nowtime - timedelta(hours = 4)
        y_begin = nowtime
        y_end = nowtime + timedelta(hours = 4)
        x=HistoryData.objects.filter(time__gte = x_begin).filter(time__lt = x_end).values_list('time').annotate(Power_Sum=Sum('power')).values_list('Power_Sum',flat=True)
        y=HistoryData.objects.filter(time__gt = y_begin).filter(time__lte = y_end).values_list('time').annotate(Power_Sum=Sum('power')).values_list('Power_Sum',flat=True)
        if len(x) == 16 and len(y) == 16:
            dataset['x_train'].append(list(x))
            dataset['y_train'].append(list(y))
        nowtime = nowtime - timedelta(minutes=15)
    return dataset

def Db2FittingData(number):
    qtest=HistoryData.objects.filter(no=number).values_list('windspeed').annotate(MaxPower=Max('power')).order_by('windspeed')
    #print(qtest.query)
    return np.array(list(qtest))