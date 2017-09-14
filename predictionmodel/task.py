from predictionmodel.prediction import train,predict
from predictionmodel.dataPreprocess import db2dataset
from predictionmodel import getData
from datetime import datetime,timedelta
from predictionmodel.models import resulttest

def trainTask():
    size = 48
    today = datetime.today()
    begtime = datetime.min
    endtime = today - timedelta(days=7)
    data = db2dataset(size,begtime,endtime)
    x = data[:, size:]
    y = data[:, :size]
    train(x,y)

def predictTask():
    size = 48
    today = datetime.today()
    yesterday = today - timedelta(days=1)
    begtime = datetime(yesterday.year,yesterday.month,yesterday.day,0,0,0)
    endtime = datetime(yesterday.year,yesterday.month,yesterday.day,23,59,59)
    data = db2dataset(size, datetime.min, endtime)
    x = data[-size:, size:]
    y = predict('knn',x)
    y = y[0].tolist()
    for i in range(0,48):
        t = begtime + timedelta(hours=i/2.0)
        r = resulttest(time=t,windspeed=y[i])
        r.save()