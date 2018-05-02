from predictionmodel.models import PredictionResult_16points,PredictionResult_288points,PredictionResult_16points1,PredictionResult_288points1,RealTime_Write
from datetime import datetime,timedelta
from predictionmodel.ReadRealtime import GetWindTower

def WriteDB_16points(predict_time,y_predict):
    PredictionResult_16points.objects.filter(DataTime__gte = predict_time).delete()
    for i in range(0,16):
        y_ = y_predict[0,i]
        if y_<0:
            y_ = 0

        obj = PredictionResult_16points(DataTime = predict_time, DataValue = y_/1000)
        obj.save()
        predict_time = predict_time + timedelta(minutes=15)

def WriteDB_16points1(predict_time,y_predict):
    PredictionResult_16points1.objects.filter(DataTime__gte = predict_time).delete()
    for i in range(0,16):
        y_ = y_predict[0,i]
        if y_<0:
            y_ = 0

        obj = PredictionResult_16points1(DataTime = predict_time, DataValue = y_/1000)
        obj.save()
        predict_time = predict_time + timedelta(minutes=15)

def WriteDB_288points(predict_time,y_predict):
    for i in range(0,288):
        try:
            obj = PredictionResult_288points.objects.get(DataTime=predict_time)
        except PredictionResult_288points.DoesNotExist:
            obj = PredictionResult_288points(DataTime = predict_time, DataValue = y_predict[0,i])
        obj.DataValue = y_predict[0,i]/1000
        obj.save()
        predict_time = predict_time + timedelta(minutes=15)

def WriteDB_288points_Naive(predict_time,y_predict):
    PredictionResult_288points.objects.filter(DataTime__gte=predict_time).delete()
    for i in range(0,288):
        y_ = y_predict[i]
        if y_<0:
            y_ = 0

        obj = PredictionResult_288points(DataTime = predict_time, DataValue = y_/1000)
        obj.save()
        predict_time = predict_time + timedelta(minutes=15)

def WriteDB_288points_Naive1(predict_time,y_predict):
    PredictionResult_288points1.objects.filter(DataTime__gte=predict_time).delete()
    for i in range(0,288):
        y_ = y_predict[i]
        if y_<0:
            y_ = 0

        obj = PredictionResult_288points1(DataTime = predict_time, DataValue = y_/1000)
        obj.save()
        predict_time = predict_time + timedelta(minutes=15)

def WriteExpect(RealTimePowerSum,Capacity,ExpectSum, UsableSum, LimitSum):
    RealTime_Write.objects.filter(DataID=40001).update(DataValue=RealTimePowerSum/1000)
    RealTime_Write.objects.filter(DataID=40002).update(DataValue=Capacity/1000)
    RealTime_Write.objects.filter(DataID=40003).update(DataValue=ExpectSum/1000)
    RealTime_Write.objects.filter(DataID=40004).update(DataValue=UsableSum/1000)
    RealTime_Write.objects.filter(DataID=40005).update(DataValue=LimitSum/1000)

def WriteWindTower():
    WindTowerInfo = GetWindTower()
    #Generation Height
    RealTime_Write.objects.filter(DataID=40006).update(DataValue=WindTowerInfo['80m_windspeed_avg'])
    RealTime_Write.objects.filter(DataID=40007).update(DataValue=WindTowerInfo['80m_dir_avg'])
    #10m
    RealTime_Write.objects.filter(DataID=40008).update(DataValue=WindTowerInfo['10m_windspeed_avg'])
    RealTime_Write.objects.filter(DataID=40009).update(DataValue=WindTowerInfo['10m_dir_avg'])
    #30m
    RealTime_Write.objects.filter(DataID=40010).update(DataValue=WindTowerInfo['30m_windspeed_avg'])
    RealTime_Write.objects.filter(DataID=40011).update(DataValue=WindTowerInfo['10m_dir_avg'])
    #50m
    RealTime_Write.objects.filter(DataID=40012).update(DataValue=WindTowerInfo['50m_windspeed_avg'])
    RealTime_Write.objects.filter(DataID=40013).update(DataValue=WindTowerInfo['10m_dir_avg'])
    #70m
    RealTime_Write.objects.filter(DataID=40014).update(DataValue=WindTowerInfo['70m_windspeed_avg'])
    RealTime_Write.objects.filter(DataID=40015).update(DataValue=WindTowerInfo['10m_dir_avg'])
    #temp,press,humidity
    #TO DO...
    RealTime_Write.objects.filter(DataID=40016).update(DataValue=WindTowerInfo['10m_temp_real'])
    RealTime_Write.objects.filter(DataID=40017).update(DataValue=WindTowerInfo['10m_hum_real'])
    RealTime_Write.objects.filter(DataID=40018).update(DataValue=WindTowerInfo['10m_press_real'])

