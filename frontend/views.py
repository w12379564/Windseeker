from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
from predictionmodel.dataQuery import getrealBytime,getpredictBytime
from predictionmodel.tasks import predictTask

# Create your views here.
def index(request):
    return render(request, 'website/index.html', context={
                      'title': 'Windseeker',
                      'welcome': 'Welcome to Steins;Gate'
                  })

def charts(request):
    return render(request, 'website/charts.html')

def tables(request):
    return render(request, 'website/tables.html')

def search_ajax(request):
    predictTask()
    beg=request.GET.get('beg',0)
    end=request.GET.get('end',0)
    begtime = datetime.strptime(beg,'%Y/%m/%d %H:%M')
    endtime = datetime.strptime(end,'%Y/%m/%d %H:%M')
    print(begtime)
    print(endtime)
    ret = []
    ret.append(getrealBytime(begtime,endtime))
    ret.append(getpredictBytime(begtime, endtime))
    print(ret)
    return JsonResponse(ret,safe=False)