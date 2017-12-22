from predictionmodel.models import PredictionResult_16points,PredictionResult_288points,RealTime
from datetime import datetime,timedelta

def WriteDB_16points(predict_time,y_predict):
    for i in range(0,16):
        try:
            obj = PredictionResult_16points.objects.get(DataTime=predict_time)
        except PredictionResult_16points.DoesNotExist:
            obj = PredictionResult_16points(DataTime = predict_time, DataValue = y_predict[0,i])
        obj.DataValue = y_predict[0,i]
        obj.save()
        predict_time = predict_time + timedelta(minutes=15)

def WriteDB_288points(predict_time,y_predict):
    for i in range(0,288):
        try:
            obj = PredictionResult_288points.objects.get(DataTime=predict_time)
        except PredictionResult_288points.DoesNotExist:
            obj = PredictionResult_288points(DataTime = predict_time, DataValue = y_predict[0,i])
        obj.DataValue = y_predict[0,i]
        obj.save()
        predict_time = predict_time + timedelta(minutes=15)

def WriteDB_288points_Naive(predict_time,y_predict):
    for i in range(0,288):
        try:
            obj = PredictionResult_288points.objects.get(DataTime=predict_time)
        except PredictionResult_288points.DoesNotExist:
            obj = PredictionResult_288points(DataTime = predict_time, DataValue = y_predict[i])
        obj.DataValue = y_predict[i]
        obj.save()
        predict_time = predict_time + timedelta(minutes=15)

def WriteExpect(ExpectSum,UsableSum,LimitSum):
    RealTime.objects.filter(DataID=40003).update(DataValue=ExpectSum)
    RealTime.objects.filter(DataID=40004).update(DataValue=UsableSum)
    RealTime.objects.filter(DataID=40005).update(DataValue=LimitSum)

