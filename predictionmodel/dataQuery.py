from . import models
from django.db.models import Sum,Max

def getrealBytime(begtime,endtime):
    q = models.weathertest.objects.filter(time__gte = begtime).filter(time__lte = endtime)
    ret = []
    for qq in q:
        ret.append(qq.windspeed/3.6)
    return ret

def getpredictBytime(begtime,endtime):
    q = models.resulttest.objects.filter(time__gte = begtime).filter(time__lte = endtime)
    ret = []
    for qq in q:
        ret.append(qq.windspeed)
    return ret

def get16p(begtime,endtime):
    q = models.PredictionResult_16points.objects.filter(DataTime__gte = begtime).filter(DataTime__lte = endtime)
    ret = []
    for qq in q:
        ret.append(qq.DataValue)

    return ret

def get288p(begtime,endtime):
    q = models.PredictionResult_288points.objects.filter(DataTime__gte = begtime).filter(DataTime__lte = endtime)
    ret = []
    for qq in q:
        ret.append(qq.DataValue)

    return ret

def getHistory(begtime,endtime):
    qq = models.HistoryData.objects.filter(time__gte=begtime).filter(time__lt=endtime).values_list('time').annotate(
        Power_Sum=Sum('power')).values_list('Power_Sum', flat=True)
    return list(qq)