from django.test import TestCase
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Windseeker.settings")
django.setup()

from frontend.models import number
from predictionmodel.dataPreprocess import db2dataset
from predictionmodel.prediction import train,predict,check
import matplotlib.pyplot as plt
from math import sqrt
from sklearn.externals import joblib
from datetime import datetime,timedelta
import predictionmodel.getData
from predictionmodel.tasks import predictTask,add,trainTask,getDataTask
from celery.schedules import crontab
from predictionmodel.dataPreprocess import Db2ShortTermData,Db2FittingData,Db2LongTermData,NetDB2Weather,GetX_Predict_LongTerm_Naive,GetX_Predict_ShortTerm
from predictionmodel.prediction import ShortTerm_Train,ShortTerm_Predictts,FittingCurve,CalExpectPower,ShortTerm_Predict,LongTerm_Train,LongTerm_Predict,LongTerm_Predict_Naive
from predictionmodel.models import HistoryData
from django.db.models import Sum
import numpy as np
from predictionmodel.models import PredictionResult_16points,WeatherData,PredictionResult_288points,RealTime_Read
from predictionmodel.ReadRealtime import GetGenerationData,GetGenerationStatus,GetWindTower
from predictionmodel.WriteRealtime import WriteExpect,WriteWindTower
from predictionmodel.dataPreprocess import Get_Realtime_WindSpeed
from predictionmodel.tasks import WindseekerTasks
from predictionmodel.models import RealTime_Write
from predictionmodel.models import Config
from predictionmodel.ReadRealtime import GetRealTimePowerSum,GetRealTimeStatus,GetGenerationData
from predictionmodel import Config_init
# Create your tests here.

def testGetdata():
    test=predictionmodel.getData.weatherHis()
    today = datetime.today()
    print(today)
    yesterday = today - timedelta(days=2)
    print(yesterday)
    data = test.getDaydata(yesterday)
    print(data)

def testTakspredict():
    predictTask()

def celeryTest():
    add.delay(3,666)

def datetest():
    today = datetime.today()
    begtime = datetime.strptime('2017-09-15 23:12', '%Y-%m-%d %H:%M')
    print(begtime)

def crontabtest():
    a = crontab(hour=9,minute=10)
    print(a.hour)

def ShortTerm_test():
    nowtime = datetime(year=2016, month=5, day=1, hour=8, minute=45)
    while nowtime < datetime(year=2016, month=5, day=16, hour=8, minute=45):
        begtime = nowtime
        endtime = nowtime + timedelta(hours=4)
        y_true = HistoryData.objects.filter(time__gt=begtime).filter(time__lte=endtime).values_list('time').annotate(Power_Sum=Sum('power')).values_list('Power_Sum', flat=True)
        y_true = np.array(list(y_true))
        y = ShortTerm_Predictts(nowtime)
        print(y_true)
        print(y)
        nowtime = nowtime + timedelta(hours=1)

def shortTerm_test():
    nowtime = datetime(year=2016,month=5,day=1,hour=6,minute=0)
    endtime = datetime(year=2016,month=5,day=17,hour=0,minute=0)
    while nowtime < endtime:
        ShortTerm_Predict(nowtime)
        nowtime = nowtime + timedelta(minutes=15)

def plot_shortterm():
    plt.ion()
    plt.close()  # clf() # 清图  cla() # 清坐标轴 close() # 关窗口
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    begtime = datetime(year=2016, month=10, day=1, hour=6, minute=15)
    endtime = datetime(year=2016, month=10, day=5, hour=3, minute=45)
    #y_predict = PredictionResult_16points.objects.filter(DataTime__gte = begtime).filter(DataTime__lte = endtime).values_list('DataValue',flat=True)
    #y_predict = np.array(list(y_predict))
    nowtime = begtime
    y16=[0]
    cnt=0
    rError=0
    aError=0
    while nowtime<endtime:
        ShortTerm_Predict(nowtime)
        qtime = nowtime + timedelta(hours=4)
        y_predict = PredictionResult_16points.objects.filter(DataTime__gte=begtime).filter(DataTime__lte=qtime).values_list('DataValue', flat=True)
        y_predict = list(y_predict)
        focus = y_predict[-16]
        focus_true = HistoryData.objects.filter(time = nowtime+timedelta(minutes=15)).values_list('time').annotate(Power_Sum=Sum('power')).values_list('Power_Sum',flat=True)
        focus_true = focus_true[0]
        y16.append(focus)
        y_true = HistoryData.objects.filter(time__gte = begtime).filter(time__lte = nowtime).values_list('time').annotate(Power_Sum=Sum('power')).values_list('Power_Sum',flat=True)
        ax.plot(y16,'b')
        ax.plot(y_true,'r')
        plt.pause(0.001)
        rError = rError + abs(focus_true-focus)/abs(focus_true)
        aError = aError + abs(focus_true-focus)/14000
        cnt = cnt + 1
        nowtime = nowtime + timedelta(minutes=15)
    print(y_predict)
    print(aError/cnt)
    print(rError/cnt)

def init_weatherdatats():
    dt = datetime(year=2016,month=5,day=1,hour=6)
    for i in range(500):
        r = WeatherData(DataTime = dt,DataID = 2,DataValue = 20)
        r.save()
        dt = dt + timedelta(minutes=15)

def longTerm_test():
    nowtime = datetime(year=2016,month=10,day=8,hour=6,minute=0)
    endtime = datetime(year=2016,month=10,day=17,hour=0,minute=0)
    while nowtime < endtime:
        LongTerm_Predict_Naive(nowtime)
        nowtime = nowtime + timedelta(days=3)

def longTerm_Naive_test():
    nowtime = datetime(year=2016,month=5,day=1,hour=6,minute=0)
    endtime = datetime(year=2016,month=5,day=17,hour=0,minute=0)
    while nowtime < endtime:
        LongTerm_Predict_Naive(nowtime)
        nowtime = nowtime + timedelta(days=1)


def plot_longterm(begtime,endtime):
    y_predict = PredictionResult_288points.objects.filter(DataTime__gte=begtime).filter(DataTime__lte=endtime).values_list('DataValue', flat=True)
    y_predict = list(y_predict)
    y_true = HistoryData.objects.filter(time__gte=begtime).filter(time__lte=endtime).values_list('time').annotate(Power_Sum=Sum('power')).values_list('Power_Sum', flat=True)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(y_predict, 'b')
    ax.plot(y_true, 'r')
    plt.show()

def init_config_windspeed():
    name = ['windspeed_real_','windspeed_avg_','windspeed_max_','windspeed_min_','windspeed_sigma_']
    #100m
    idx=10001
    for i in range(0,5):
        CONFIG = Config(DataID=idx+i,configname=name[i]+'100m')
        CONFIG.save()
    #90m
    idx=10006
    for i in range(0,5):
        CONFIG = Config(DataID=idx+i,configname=name[i]+'90m')
        CONFIG.save()
    #80m
    idx=10011
    for i in range(0,5):
        CONFIG = Config(DataID=idx+i,configname=name[i]+'80m')
        CONFIG.save()
    #70m
    idx=10016
    for i in range(0,5):
        CONFIG = Config(DataID=idx+i,configname=name[i]+'70m')
        CONFIG.save()
    #50m
    idx=10021
    for i in range(0,5):
        CONFIG = Config(DataID=idx+i,configname=name[i]+'50m')
        CONFIG.save()
    #30m
    idx=10026
    for i in range(0,5):
        CONFIG = Config(DataID=idx+i,configname=name[i]+'30m')
        CONFIG.save()
    #10m
    idx=10031
    for i in range(0,5):
        CONFIG = Config(DataID=idx+i,configname=name[i]+'10m')
        CONFIG.save()


def init_config_winddir():
    name = ['dir_real_', 'dir_avg_', 'dir_max_', 'dir_min_', 'dir_sigma_']
    CONFIG = Config(DataID=10036, configname='null')
    CONFIG.save()
    #100m
    idx=10037
    for i in range(0,5):
        CONFIG = Config(DataID=idx+i,configname=name[i]+'100m')
        CONFIG.save()
    #90m
    idx=10042
    for i in range(0,5):
        CONFIG = Config(DataID=idx+i,configname=name[i]+'90m')
        CONFIG.save()
    #80m
    idx=10047
    for i in range(0,5):
        CONFIG = Config(DataID=idx+i,configname=name[i]+'80m')
        CONFIG.save()
    #10m
    idx=10052
    for i in range(0,5):
        CONFIG = Config(DataID=idx+i,configname=name[i]+'10m')
        CONFIG.save()


def init_config_gendata():
    name = ['windspeed','power','reactivate power','voltage','current','frequency','null','null','null','null']
    for i in range(20001, 20241):
        idx = (i-20001)%10
        r = Config(DataID = i,configname = name[idx])
        r.save()

def init_config_genstatus():
    name = ['stopping','running','error','waiting','null']
    for i in range(30001,30121):
        idx = (i - 30001) % 5
        r = Config(DataID = i,configname = name[idx])
        r.save()

def init_realtime():
    Items = Config.objects.all()
    for item in Items:
        r = RealTime_Read(DataID = item.DataID,DataValue = item.DataID)
        r.save()

# Run here.
nowtime = datetime(2017,10,10)
GetX_Predict_ShortTerm(nowtime)
