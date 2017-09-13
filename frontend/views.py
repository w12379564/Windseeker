from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from frontend.models import number
from predictionmodel.prediction import predict
from sklearn.externals import joblib

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
    id=int(request.GET['a'])
    ret=[]
    x_test = joblib.load('predictionmodel/data/'+'x_test.data')
    y_target = joblib.load('predictionmodel/data/'+'y_target.data')
    y_predict = predict('knn',x_test[id])
    ret.append(y_target[id].tolist())
    ret.append(y_predict[0].tolist())
    #print(ret)
    return JsonResponse(ret,safe=False)