from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.contrib import admin
from . import views
# from parser import MangaPandaParser
from tomabi_app.forms import LoginForm

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^accounts/login/', auth_views.login, {'authentication_form': LoginForm}, name='login'),
    url(r'^accounts/logout/', auth_views.logout, name='logout'),
    url('^accounts/', include('django.contrib.auth.urls')),
    url(r'^mymangas/$', views.mymangas, name='mymangas'),
    url(r'^mymangas/add/$', views.addmangas, name='addmangas'),
    url(r'^mymangas/delete/(?P<id>\d+)/$', views.deletemangas, name='deletemangas'),
    url(r'^mymangas/reset/(?P<id>\d+)/$', views.resetmangas, name='resetmangas'),
    url(r'^mymangas/read/(?P<id>\d+)/(?P<chapter>\d+)$', views.markasread, name='markasread'),
    url(r'^mymangas/refresh/$', views.refresh, name='refresh'),
    url(r'^myprogress/$', views.myprogress, name='myprogress'),

 ]
