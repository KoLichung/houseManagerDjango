from django.urls import path

from ecpayApp import views

app_name = 'ecpayApp'

urlpatterns = [
    path('ecpay/', views.ecpay_view, name='ecpay'),
]