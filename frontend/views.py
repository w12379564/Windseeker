from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

# Create your views here.
def index(request):
    return render(request, 'website/index.html', context={
                      'title': '命运石之门的选择',
                      'welcome': 'Welcome to Steins;Gate'
                  })

def charts(request):
    return render(request, 'website/charts.html')

def tables(request):
    return render(request, 'website/tables.html')

def search_ajax(request):
    ret=[12,11,10,9,8,7,6,5,4,3,2,1]
    return JsonResponse(ret,safe=False)