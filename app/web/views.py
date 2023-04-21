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
            return redirect('/login')
    return render(request,'web/login.html')

def register(request):
    
    phone = request.GET.get('phone')

    if request.method == 'POST' and 'register'in request.POST :
        print('register button clicked')
        username = request.POST['name']
        phone = request.POST['phone']
        password = request.POST['password']
        if User.objects.filter(phone=phone).exists() != False:
            print('user 已存在')
            user = authenticate(request, phone=phone, password=password)
            if user is not None and user.nickname == username :
                auth.login(request, user)
                return redirect('/backboard/',{'user':user})
            else:
                return render(request, 'web/register.html',{'alert_flag': True})
        else:
            print('建立新user')
            user = User()
            user.nickname = username
            user.phone = phone
            user.set_password(password)
            user.save()
            auth.login(request, user)
            print(request.user)
            print('3')
            return redirect('/backboard/',{'user':user})

    return render(request,'web/register.html')

def pricing(request):
    return render(request,'web/pricing.html')

def housemanager(request):
    id = request.GET.get('manager')
    user = User.objects.get(id=id)
    return render(request,'web/housemanager.html',{'user':user})