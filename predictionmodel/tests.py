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
from predictionmodel.prediction import ShortTerm_Train,ShortTerm_Predictts,FittingCurve,CalExpectPower
from predictionmodel.models import HistoryData
from django.db.models import Sum
import numpy as np
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

# Run here.
#ShortTerm_Train()
