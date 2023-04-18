from django.shortcuts import redirect, render
from django.http import HttpResponse

# Create your views here.

def top_video(request):
    return render(request,'backboard/top_video.html')

def main_image(request):
    return render(request,'backboard/main_image.html')

def about(request):
    return render(request,'backboard/about.html')

def testimonial(request):
    return render(request,'backboard/testimonial.html')

def cases(request):
    return render(request,'backboard/cases.html')

def faq(request):
    return render(request,'backboard/faq.html')

def new_edit_faq(request):
    return render(request,'backboard/new_edit_faq.html')

def advert_setting(request):
    return render(request,'backboard/advert_setting.html')

def bills(request):
    return render(request,'backboard/bills.html')

def setting(request):
    return render(request,'backboard/setting.html')
