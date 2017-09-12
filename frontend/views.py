from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from frontend.models import number

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
    ret=[]
    for n in number.objects.all():
        ret.append(n.value)
    return JsonResponse(ret,safe=False)