from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth import authenticate
# Create your views here.

def index(request):
    return render(request,'web/index.html')

def login(request):
    if request.method == 'POST':
        name = request.POST['name']
        password = request.POST['password']
        user = authenticate(request, name=name, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/backboard/',{'user':user})
        else:
            return redirect('/')
    return render(request,'web/login.html')

def register(request):
    return render(request,'web/register.html')

def pricing(request):
    return render(request,'web/pricing.html')

