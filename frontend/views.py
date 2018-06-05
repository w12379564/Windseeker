from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
from predictionmodel.dataQuery import getrealBytime,getpredictBytime,get16p,getHistory,get288p
from predictionmodel.tasks import predictTask,getDataTask
from predictionmodel.excel2db import read_xlsx1

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

def getdata_ajax(request):
    getDataTask()
    return JsonResponse("OK", safe=False)

def predict_ajax(request):
    predictTask()
    return JsonResponse("OK", safe=False)

def upload_history(request):
    print("123")
    if request.method == "POST":
        myFile =request.FILES.get("myfile", None)
        if myFile!=None:
            read_xlsx1(myFile)
    return JsonResponse("upload over", safe=False)

def shortp(request):
    return render(request, 'website/shortp.html')

def get16p_ajax(request):
    beg=request.GET.get('beg',0)
    end=request.GET.get('end',0)
    begtime = datetime.strptime(beg,'%Y/%m/%d %H:%M')
    endtime = datetime.strptime(end,'%Y/%m/%d %H:%M')
    print(begtime)
    print(endtime)
    ret = []

    ret.append({'name':'预测值','data':get16p(begtime,endtime)})
    ret.append({'name':'实际值','data':getHistory(begtime,endtime)})

    print(ret)
    return JsonResponse(ret,safe=False)

def longp(request):
    return render(request, 'website/longp.html')

def get288p_ajax(request):
    beg=request.GET.get('beg',0)
    end=request.GET.get('end',0)
    begtime = datetime.strptime(beg,'%Y/%m/%d %H:%M')
    endtime = datetime.strptime(end,'%Y/%m/%d %H:%M')
    print(begtime)
    print(endtime)
    ret = []

    ret.append({'name':'预测值','data':get288p(begtime,endtime)})
    ret.append({'name':'实际值','data':getHistory(begtime,endtime)})

    print(ret)
    return JsonResponse(ret,safe=False)