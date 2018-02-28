from predictionmodel.models import HistoryData,RealTime_Read
from predictionmodel.models import Config
from datetime import datetime
from django.db.models import Q

#Generation number
GenerationNumber = 62

def GetGenerationData(nowtime):
    InsertTime = datetime(year=nowtime.year,month=nowtime.month,day=nowtime.day,hour=nowtime.hour,minute=nowtime.minute)
    #print(InsertTime)
    for no in range(1,GenerationNumber+1):
        wsp_id = Config.objects.get(configname =str(no) + '#windspeed').DataID
        power_id = Config.objects.get(configname =str(no) + '#power').DataID
        wsp = RealTime_Read.objects.get(DataID=wsp_id).DataValue/10000
        power = RealTime_Read.objects.get(DataID=power_id).DataValue
        try:
            newrecord = HistoryData.objects.get(time=InsertTime, no=no)
        except HistoryData.DoesNotExist:
            newrecord = HistoryData(time=InsertTime, no=no, power=power, windspeed=wsp)
            newrecord.save()

#If a generation has a positive power output, we think it is running
def GetRealTimeStatus():
    RunningStatus = []
    #RtItems = RealTime_GenerationData.objects.filter(DataID__gte=20001).filter(DataID__lte=20240)
    for no in range(1, GenerationNumber + 1):
        power_id = Config.objects.get(configname=str(no) + '#power').DataID
        power = RealTime_Read.objects.get(DataID=power_id).DataValue
        if power > 0:
            RunningStatus.append(1)
        else:
            RunningStatus.append(0)
    return RunningStatus

def GetRealTimePowerSum():
    #RtItems = RealTime_GenerationData.objects.filter(DataID__gte=20001).filter(DataID__lte=20240)
    RealTimePowerSum = 0
    for no in range(1, GenerationNumber + 1):
        power_id = Config.objects.get(configname=str(no) + '#power').DataID
        power = RealTime_Read.objects.get(DataID=power_id).DataValue
        RealTimePowerSum = RealTimePowerSum + power
    #print(RealTimePowerSum)
    return RealTimePowerSum

#useless
def GetGenerationStatus():
    RtItems = RealTime_Read.objects.filter(DataID__gte=30001).filter(DataID__lte=30120)
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
    WindTowerItems = Config.objects.filter(Q(configname__contains = '_windspeed')| Q(configname__contains = '_dir')
                                           | Q(configname__contains='_temp') | Q(configname__contains = '_hum')
                                           | Q(configname__contains='_press'))
    WindTowerInfo={}
    for items in WindTowerItems:
        WindTowerInfo[items.configname] = RealTime_Read.objects.get(DataID = items.DataID).DataValue
    return WindTowerInfo