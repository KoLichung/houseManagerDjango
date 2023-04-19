from django.shortcuts import redirect, render
from django.http import HttpResponse
from modelCore.models import User, FAQ
import urllib
import datetime
from modelCore.forms import FAQForm
from django.contrib import auth
from django.contrib.auth import authenticate

# Create your views here.

def logout(request):
    auth.logout(request)
    return redirect('/')


def top_video(request):
    
    user = request.user
    if request.method == 'POST':

        user.video_link = request.POST.get('video_link')
        user.video_title = request.POST.get('video_title')
        user.video_subtitle = request.POST.get('video_subtitle')
        user.save()
        
        return redirect_params('top_video',{'user':user})

    return render(request,'backboard/top_video.html',{'user':user})

def main_image(request):
    return render(request,'backboard/main_image.html')

def about(request):

    user = request.user
    if request.method == 'POST':

        user.nickname = request.POST.get('nickname')
        user.phone_number = request.POST.get('phone_number')
        user.line_id = request.POST.get('line_id')
        user.about_me = request.POST.get('about_me')

        user.save()
        
        return redirect_params('about',{'user':user})

    return render(request,'backboard/about.html',{'user':user})

def testimonial(request):
    return render(request,'backboard/testimonial.html')

def cases(request):

    user = request.user
    if request.method == 'POST':
        user.case_link = request.POST.get('case_link')
        user.save()
        return redirect_params('cases',{'user':user})

    return render(request,'backboard/cases.html',{'user':user})

def faq(request):
   
    return render(request,'backboard/faq.html')

def new_edit_faq(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/backboard/')

    if request.method == 'POST':
        
        if request.GET.get('post_id') != None:
            assistancePost = FAQ.objects.get(id=request.GET.get('post_id'))
        else:
            assistancePost = FAQ()
            assistancePost.create_date = datetime.datetime.now()

        assistancePost.title = request.POST.get('title') 
        assistancePost.body = request.POST.get('body') 
        
        
        if assistancePost.title != None and assistancePost.title != '':

            if request.FILES.get('cover_image', False):
                assistancePost.cover_image = request.FILES['cover_image']

            assistancePost.save()

        return redirect('all_assistances')

    if request.GET.get('post_id') != None:
        assistancePost = FAQ.objects.get(id=request.GET.get('post_id'))
        form = FAQForm(instance=assistancePost)
        return render(request, 'backboard/new_assistance.html', { 'post':assistancePost,'form':form})

    form = FAQForm()
    return render(request,'backboard/new_edit_faq.html', {'form':form})

def advert_setting(request):
    user = request.user
    if request.method == 'POST':
        user.fb_pixel = request.POST.get('fb_pixel')
        user.google_id = request.POST.get('google_id')
        user.save()
        return redirect_params('advert_setting',{'user':user})

    return render(request,'backboard/advert_setting.html',{'user':user})

def bills(request):
    return render(request,'backboard/bills.html')

def setting(request):
    return render(request,'backboard/setting.html')


def redirect_params(url, params=None):
    response = redirect(url)
    if params:
        query_string = urllib.parse.urlencode(params)
        response['Location'] += '?' + query_string
    return response