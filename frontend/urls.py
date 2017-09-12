from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'index', views.index, name='index'),
    url(r'charts', views.charts, name='charts'),
    url(r'tables', views.tables, name='tables'),
    url(r'^search_ajax/$', views.search_ajax, name='search_ajax')
]