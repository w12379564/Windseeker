from predictionmodel.models import RealTime,Config,HistoryData
from datetime import datetime

def GetGenerationData():
    nowtime = datetime.now()
    InsertTime = datetime(year=nowtime.year,month=nowtime.month,day=nowtime.day,hour=nowtime.hour,minute=nowtime.minute)
    #print(InsertTime)
    RtItems = RealTime.objects.filter(DataID__gte = 20001).filter(DataID__lte = 20240)
    toInsert=[]
    for i in range(0,240,10):
        toInsert.append(HistoryData(time=InsertTime,no=i/10+1,windspeed=RtItems[i].DataValue,power=RtItems[i+1].DataValue))
    HistoryData.objects.bulk_create(toInsert)

def GetGenerationInfo():
    RtItems = RealTime.objects.filter(DataID__gte=30001).filter(DataID__lte=30120)
    ret=[]
    for i in range(0,120,5):
        Info={RtItems[i].config.configname: RtItems[i].DataValue,
              RtItems[i+1].config.configname: RtItems[i+1].DataValue,
              RtItems[i+2].config.configname: RtItems[i+2].DataValue,
              RtItems[i+3].config.configname: RtItems[i+3].DataValue,
              RtItems[i+4].config.configname: RtItems[i+4].DataValue}
        ret.append(Info)
    print(ret)