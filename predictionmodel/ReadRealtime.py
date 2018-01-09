from predictionmodel.models import HistoryData,RealTime_GenerationStatus,RealTime_GenerationData,RealTime_WindTower
from predictionmodel.models import Config
from datetime import datetime

def GetGenerationData(nowtime):
    InsertTime = datetime(year=nowtime.year,month=nowtime.month,day=nowtime.day,hour=nowtime.hour,minute=nowtime.minute)
    #print(InsertTime)
    RtItems = RealTime_GenerationData.objects.filter(DataID__gte = 20001).filter(DataID__lte = 20240)
    for i in range(0,240,10):
        t = InsertTime
        number = i/10+1
        wsp = RtItems[i].DataValue
        p = RtItems[i + 1].DataValue
        try:
            newrecord = HistoryData.objects.get(time=t,no=number)
        except HistoryData.DoesNotExist:
            newrecord = HistoryData(time=t, no=number, power=p, windspeed=wsp)
            newrecord.save()

#If a generation has a positive power output, we think it is running
def GetRealTimeStatus():
    RunningStatus = []
    RtItems = RealTime_GenerationData.objects.filter(DataID__gte=20001).filter(DataID__lte=20240)
    for i in range(0, 240, 10):
        if RtItems[i + 1].DataValue > 0:
            RunningStatus.append(1)
        else:
            RunningStatus.append(0)
    return RunningStatus

def GetRealTimePowerSum():
    RtItems = RealTime_GenerationData.objects.filter(DataID__gte=20001).filter(DataID__lte=20240)
    RealTimePowerSum = 0
    for i in range(0, 240, 10):
        RealTimePowerSum = RealTimePowerSum + RtItems[i + 1].DataValue
    #print(RealTimePowerSum)
    return RealTimePowerSum


def GetGenerationStatus():
    RtItems = RealTime_GenerationStatus.objects.filter(DataID__gte=30001).filter(DataID__lte=30120)
    RtConfigs = Config.objects.filter(DataID__gte=30001).filter(DataID__lte=30120)
    ret=[]
    for i in range(0,120,5):
        Status={RtConfigs[i].configname: RtItems[i].DataValue,
                RtConfigs[i+1].configname: RtItems[i+1].DataValue,
                RtConfigs[i+2].configname: RtItems[i+2].DataValue,
                RtConfigs[i+3].configname: RtItems[i+3].DataValue,
                RtConfigs[i+4].configname: RtItems[i+4].DataValue}
        ret.append(Status)
    #print(ret)
    return ret

def GetWindTower():
    RtItems = RealTime_WindTower.objects.filter(DataID__gte=10001).filter(DataID__lte=10056)
    RtConfigs = Config.objects.filter(DataID__gte=10001).filter(DataID__lte=10056)
    len1 = len(RtItems)
    len2 = len(RtConfigs)
    l = min(len1,len2)
    WindTowerInfo={}
    for i in range(l):
        WindTowerInfo[RtConfigs[i].configname] = RtItems[i].DataValue
    #print(WindTowerInfo)
    return WindTowerInfo