from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'index', views.index, name='index'),
    url(r'charts', views.charts, name='charts'),
    url(r'tables', views.tables, name='tables'),
    url(r'^search_ajax/$', views.search_ajax, name='search_ajax'),
    url(r'^getdata_ajax/$', views.getdata_ajax, name='getdata_ajax'),
    url(r'^predict_ajax/$', views.predict_ajax, name='predict_ajax'),
    url(r'^upload_history/$', views.upload_history, name='upload_history'),
    url(r'shortp', views.shortp, name='shortp'),
    url(r'^get16p_ajax/$', views.get16p_ajax, name='get16p_ajax'),
    url(r'longp', views.longp, name='longp'),
    url(r'^get288p_ajax/$', views.get288p_ajax, name='get288p_ajax')
]