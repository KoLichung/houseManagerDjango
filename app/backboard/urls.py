from django.urls import path, include
from . import views
from django.shortcuts import render
from django.http import HttpResponse

urlpatterns = [
    path('', views.top_video, name = 'top_video'), 
    path('main_image', views.main_image, name = 'main_image'), 
    path('about', views.about, name = 'about'), 
    path('testimonial', views.testimonial, name = 'testimonial'), 
    path('cases', views.cases, name = 'cases'), 
    path('faq', views.faq, name = 'faq'), 
    path('new_edit_faq', views.new_edit_faq, name = 'new_edit_faq'), 
    path('advert_setting', views.advert_setting, name = 'advert_setting'), 
    path('bills', views.bills, name = 'bills'), 
    path('plans', views.plans, name = 'plans'), 
    path('upgrade', views.upgrade, name = 'upgrade'), 
    path('setting', views.setting, name = 'setting'), 
    path('logout', views.logout, name='backboard_logout'),
]