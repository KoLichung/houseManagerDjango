from django.urls import path, include
from . import views
from django.shortcuts import render
from django.http import HttpResponse

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('pricing', views.pricing, name='pricing'),
    path('housemanager', views.housemanager, name='housemanager'),
]