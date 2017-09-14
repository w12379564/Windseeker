from . import models

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
