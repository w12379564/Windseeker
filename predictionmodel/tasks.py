from __future__ import absolute_import, unicode_literals
from predictionmodel.prediction import train,predict
from predictionmodel.dataPreprocess import db2dataset
from datetime import datetime,timedelta
from predictionmodel.models import resulttest,celerytest
import predictionmodel.getData
from . import models
from celery import shared_task
from predictionmodel.prediction import ShortTerm_Predict,LongTerm_Predict_Naive,CalExpectPower
from predictionmodel.ReadRealtime import GetGenerationData
from predictionmodel.WriteRealtime import WriteWindTower

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

@shared_task
def Predict():
    nowtime = datetime.today()
    #timestap = datetime(year=nowtime.year, month=nowtime.month, day=nowtime.day,hour=nowtime.hour,minute=nowtime.minute)
    timestap = datetime(year=nowtime.year-1, month=nowtime.month-6, day=nowtime.day,hour=nowtime.hour,minute=nowtime.minute)
    ShortTerm_Predict(timestap)
    LongTerm_Predict_Naive(timestap)


@shared_task
def GetData():
    nowtime = datetime.today()
    #timestap = datetime(year=nowtime.year, month=nowtime.month, day=nowtime.day,hour=nowtime.hour,minute=nowtime.minute)
    timestap = datetime(year=nowtime.year-1, month=nowtime.month-6, day=nowtime.day,hour=nowtime.hour,minute=nowtime.minute)
    GetGenerationData(timestap)
    print("done")


@shared_task
def CalcExpectValue_WriteRT():
    WriteWindTower()
    CalExpectPower()

@shared_task
def WindseekerTasks():
    nowtime = datetime.today()
    #timestap = datetime(year=nowtime.year, month=nowtime.month, day=nowtime.day,hour=nowtime.hour,minute=nowtime.minute)
    timestap = datetime(year=nowtime.year-1, month=nowtime.month-6, day=nowtime.day,hour=nowtime.hour,minute=nowtime.minute)
    #Write WindTower data
    WriteWindTower()
    #from realtime to db
    GetGenerationData(timestap)

    CalExpectPower()

    ShortTerm_Predict(timestap)

    LongTerm_Predict_Naive(timestap)