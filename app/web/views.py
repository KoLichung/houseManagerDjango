from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth import authenticate
from modelCore.models import User, HouseCase, FAQ
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
        nickname = request.POST['nickname']
        phone = request.POST['phone']
        password = request.POST['password']
        if User.objects.filter(phone=phone).exists() != False:
            print('user 已存在')
            user = authenticate(request, phone=phone, password=password)
            if user is not None and user.nickname == nickname :
                auth.login(request, user)
                return redirect('/backboard/',{'user':user})
            else:
                return render(request, 'web/register.html',{'alert_flag': True})
        else:
            print('建立新user')
            user = User()
            user.nickname = nickname
            user.phone = phone
            user.set_password(password)
            user.save()
            auth.login(request, user)
           
            return redirect('/backboard/',{'user':user})

    return render(request,'web/register.html')

def pricing(request):
    return render(request,'web/pricing.html')

def housemanager_demo(request):

    return render(request,'web/housemanager_demo.html')

def housemanager(request):
    manager_id = request.GET.get('manager')
    if manager_id is not None:
        user = User.objects.get(id=manager_id)
        user_shop_id = user.case_link.replace('https://www.591.com.tw/broker','')
        cases = HouseCase.objects.filter(shop_id=user_shop_id)
        faqs = FAQ.objects.filter(user=user).order_by('-id')
        print(user_shop_id)
       
        
    else:
        user = None

    return render(request,'house_manager/housemanager.html',{
        'user':user, 
        'cases':cases,
        'faqs':faqs})
