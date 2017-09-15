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
from predictionmodel.tasks import predictTask,add
from celery.schedules import crontab
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

# Run here.
crontabtest()