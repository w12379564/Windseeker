from predictionmodel.models import RealTime,Config,HistoryData
from datetime import datetime

def GetGenerationData():
    nowtime = datetime.now()
    InsertTime = datetime(year=nowtime.year,month=nowtime.month,day=nowtime.day,hour=nowtime.hour,minute=nowtime.minute)
    print(InsertTime)
    RtItems = RealTime.objects.filter(DataID__gte = 20001).filter(DataID__lte = 20240)
    toInsert=[]
    for i in range(0,240,10):
        toInsert.append(HistoryData(time=InsertTime,no=i/10+1,windspeed=RtItems[i].DataValue,power=RtItems[i+1].DataValue))
    HistoryData.objects.bulk_create(toInsert)