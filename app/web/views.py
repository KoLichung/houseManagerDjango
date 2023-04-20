from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth import authenticate
from modelCore.models import User
# Create your views here.

def index(request):
    return render(request,'web/index.html')

def login(request):
    if request.method == 'POST':
        phone = request.POST['phone']
        password = request.POST['password']
        user = authenticate(request, phone=phone, password=password)
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

def housemanager(request):
    id = request.GET.get('manager')
    user = User.objects.get(id=id)
    return render(request,'web/housemanager.html',{'user':user})