from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request,'web/index.html')

def login(request):
    return render(request,'web/login.html')

def register(request):
    return render(request,'web/register.html')

def pricing(request):
    return render(request,'web/pricing.html')

