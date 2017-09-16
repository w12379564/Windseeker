from __future__ import absolute_import, unicode_literals
from predictionmodel.prediction import train,predict
from predictionmodel.dataPreprocess import db2dataset
from datetime import datetime,timedelta
from predictionmodel.models import resulttest,celerytest
import predictionmodel.getData
from . import models
from celery import shared_task

@shared_task
def trainTask():
    size = 48
    today = datetime.today()
    begtime = datetime.min
    endtime = today - timedelta(days=7)
    data = db2dataset(size,begtime,endtime)
    x = data[:, size:]
    y = data[:, :size]
    train(x,y)

@shared_task
def predictTask():
    size = 48
    today = datetime.today()
    yesterday = today - timedelta(days=1)
    begtime = datetime(yesterday.year,yesterday.month,yesterday.day,0,0,0)
    endtime = datetime(yesterday.year,yesterday.month,yesterday.day,23,59,59)

    q = models.resulttest.objects.filter(time__gte=begtime).filter(time__lte=endtime)
    if len(q) == 0:
        getobj = predictionmodel.getData.weatherHis()
        getobj.getDaydata(begtime)

    data = db2dataset(size, begtime, endtime)

    x = data[:,size:]
    y = predict('knn',x)
    y = y[0].tolist()

    for i in range(0,48):
        t = begtime + timedelta(hours=i/2.0)
        r = resulttest(time=t,windspeed=y[i])
        r.save()

@shared_task
def getDataTask():
    today = datetime.today()
    yesterday = today - timedelta(days=1)
    getobj = predictionmodel.getData.weatherHis()
    getobj.getDaydata(yesterday)

@shared_task
def add(x, y):
    print(x+y)

@shared_task
def writedbtest():
    t = datetime.now()
    r = celerytest(time=t)
    r.save()