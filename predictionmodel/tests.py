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
from predictionmodel.tasks import predictTask,add,trainTask
from celery.schedules import crontab
from predictionmodel.dataPreprocess import Db2ShortTermData,Db2FittingData
from predictionmodel.prediction import ShortTerm_Train,ShortTerm_Predictts,FittingCurve,CalExpectPower,ShortTerm_Predict
from predictionmodel.models import HistoryData
from django.db.models import Sum
import numpy as np
from predictionmodel.models import RealTime,Config
from predictionmodel.Realtime2DB import GetGenerationData,GetGenerationInfo
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

def init_realtime():
    for i in range(40001,40019):
        r = RealTime(DataID=i,DataValue=i)
        r.save()

def init_config_gendata():
    name = ['windspeed','power','reactivate power','voltage','current','frequency','null','null','null','null']
    for i in range(20001, 20241):
        rtItem = RealTime.objects.get(DataID=i)
        idx = (i-20001)%10

        r = Config(RealtimeItem = rtItem,configname = name[idx])
        r.save()

def init_config_geninfo():
    name = ['stopping','running','error','waiting','null']
    for i in range(30001,30121):
        rtItem = RealTime.objects.get(DataID=i)
        idx = (i - 30001) % 5
        r = Config(RealtimeItem=rtItem, configname=name[idx])
        r.save()

def shortTerm_test():
    nowtime = datetime(year=2016,month=5,day=1,hour=6,minute=0)
    endtime = datetime(year=2016,month=5,day=17,hour=0,minute=0)
    while nowtime < endtime:
        ShortTerm_Predict(nowtime)
        nowtime = nowtime + timedelta(minutes=15)

# Run here.
shortTerm_test()