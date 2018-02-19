import numpy as np
from predictionmodel.models import weathertest
from django.db.models import Sum
from datetime import datetime,timedelta
from predictionmodel.models import HistoryData,WeatherData,RealTime_Read,Config
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
        x=HistoryData.objects.filter(time__gte = x_begin).filter(time__lt = x_end).values_list('time').annotate(Power_Sum=Sum('power')).values_list('Power_Sum',flat=True).order_by('time')
        print(list(x))
        y=HistoryData.objects.filter(time__gt = y_begin).filter(time__lte = y_end).values_list('time').annotate(Power_Sum=Sum('power')).values_list('Power_Sum',flat=True).order_by('time')
        if len(x) == 16 and len(y) == 16:
            dataset['x_train'].append(list(x))
            dataset['y_train'].append(list(y))
        nowtime = nowtime - timedelta(minutes=15)
    return dataset

def Db2FittingData(number):
    qtest=HistoryData.objects.filter(no=number).values_list('windspeed').annotate(MaxPower=Max('power')).order_by('windspeed')
    #print(qtest.query)
    return np.array(list(qtest))

def Db2LongTermData(begtime,endtime):
    dataset = {'x_train': [], 'y_train': []}
    nt = endtime
    while nt>begtime:
        et = nt
        bt = et - timedelta(days=3)
        x = []
        for i in range(1,5):
            x_sub = WeatherData.objects.filter(DataID=i).filter(DataTime__gte = bt).filter(DataTime__lt = et).values_list("DataValue",flat=True).order_by('DataTime')
            x = x + list(x_sub)
        y = HistoryData.objects.filter(time__gte=bt).filter(time__lt=et).values_list('time').annotate(Power_Sum=Sum('power')).values_list('Power_Sum', flat=True).order_by('time')
        y = list(y)
        if len(x)==4*288 and len(y)==288:
            dataset['x_train'].append(x)
            dataset['y_train'].append(y)
        nt = nt - timedelta(days=3)
    return dataset

def NetDB2Weather(bt,et):
    #ID 1 windspeed
    #ID 2 temperature
    #ID 3 humidity
    #ID 4 press
    netdata = weathertest.objects.filter(time__gte=bt).filter(time__lt=et)
    weatherlist=[]
    for r in netdata:
        weatherlist.append(WeatherData(DataTime=r.time,DataID=1,DataValue=r.windspeed/3.6))
        weatherlist.append(WeatherData(DataTime=r.time+timedelta(minutes=15), DataID=1, DataValue=r.windspeed/3.6))
        weatherlist.append(WeatherData(DataTime=r.time,DataID=2,DataValue=r.temp))
        weatherlist.append(WeatherData(DataTime=r.time+timedelta(minutes=15), DataID=2, DataValue=r.temp))
        weatherlist.append(WeatherData(DataTime=r.time,DataID=3,DataValue=r.hum))
        weatherlist.append(WeatherData(DataTime=r.time+timedelta(minutes=15), DataID=3, DataValue=r.hum))
        weatherlist.append(WeatherData(DataTime=r.time,DataID=4,DataValue=r.press))
        weatherlist.append(WeatherData(DataTime=r.time+timedelta(minutes=15), DataID=4, DataValue=r.press))
    WeatherData.objects.bulk_create(weatherlist)

def GetX_Predict_LongTerm(nowtime):
    nowtime = datetime(year=nowtime.year, month=nowtime.month, day=nowtime.day,hour=nowtime.hour,minute=nowtime.minute)
    bt = nowtime + timedelta(minutes=15)
    et = bt + timedelta(days=3)
    x = []
    for i in range(1, 5):
        x_sub = WeatherData.objects.filter(DataID=i).filter(DataTime__gte=bt).filter(DataTime__lt=et).values_list(
            "DataValue", flat=True).order_by('DataTime')
        x = x + list(x_sub)
    return x

def GetX_Predict_LongTerm_Naive(nowtime):
    nowtime = datetime(year=nowtime.year, month=nowtime.month, day=nowtime.day,hour=nowtime.hour,minute=nowtime.minute)
    bt = nowtime + timedelta(minutes=15)
    et = bt + timedelta(days=3)
    x_sub = WeatherData.objects.filter(DataID=1).filter(DataTime__gte=bt).filter(DataTime__lt=et).values_list(
            "DataValue", flat=True).order_by('DataTime')

    ret = list(x_sub)
    while len(ret)<288:
        if len(ret)>0:
            ret.append(ret[-1])
        else:
            ret.append(0)

    if len(ret)>288:
        ret = ret[-288:]
    return ret

def GetX_Predict_ShortTerm(nowtime):
    nowtime = datetime(year=nowtime.year, month=nowtime.month, day=nowtime.day,hour=nowtime.hour,minute=nowtime.minute)
    endtime = nowtime
    begtime = endtime - timedelta(hours=4)
    x = HistoryData.objects.filter(time__gte=begtime).filter(time__lt=endtime).values_list('time').annotate(Power_Sum=Sum('power')).values_list('Power_Sum', flat=True).order_by('time')
    ret=list(x)
    while len(ret)<16:
        if len(ret)>0:
            ret.append(ret[-1])
        else:
            ret.append(0)

    if len(ret)>16:
        ret = ret[-16:]
    return ret

def Get_Realtime_WindSpeed():
    #70m windspeed avg
    ID = Config.objects.get(configname = '70m_windspeed_avg').DataID
    ret = RealTime_Read.objects.filter(DataID=ID).values_list('DataValue',flat=True)
    ret = float(ret[0])
    return ret