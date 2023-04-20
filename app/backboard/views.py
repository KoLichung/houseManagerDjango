from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.http import HttpResponse
from modelCore.models import User, FAQ
import urllib
import datetime
from modelCore.forms import AboutForm, TestimonialForm, UserMainImageForm
from django.contrib import auth
from django.contrib.auth import authenticate

# Create your views here.

def logout(request):
    auth.logout(request)
    return redirect('/')

def top_video(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/')
    user = request.user
    if request.method == 'POST':

        user.video_link = request.POST.get('video_link')
        user.video_title = request.POST.get('video_title')
        user.video_subtitle = request.POST.get('video_subtitle')
        user.save()
        
        return redirect_params('top_video',{'user':user})

    return render(request,'backboard/top_video.html',{'user':user})

def main_image(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/')
    # user = request.user 
    # userform = UserMainImageForm()
    # if request.method == 'POST' :
    #     userform = UserMainImageForm(request.POST or None, request.FILES or None, instance=user)
    #     if userform.is_valid():
    #         print('valid')
    #         user = userform.save(commit=False)
    #         user.save()
    #     user = userform.instance
    #     user.save()

    # return render(request,'backboard/main_image.html',{'user':user,'userform':userform})
    return render(request,'backboard/main_image.html')

def about(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/')

    user = request.user
    if request.method == 'POST':

        user.nickname = request.POST.get('nickname')
        user.phone_number = request.POST.get('phone_number')
        user.line_id = request.POST.get('line_id')
        user.about_me = request.POST.get('about_me')

        user.save()
        
        return redirect_params('about',{'user':user})
    
    form = AboutForm()
    return render(request,'backboard/about.html',{'user':user, 'form':form})

def testimonial(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/')
    user = request.user
    form = TestimonialForm()
    return render(request,'backboard/testimonial.html',{'user':user,'form':form} )

def cases(request):
    if not request.user.is_authenticated or not request.user.is_staff:
            return redirect('/')
    user = request.user
    if request.method == 'POST':
        user.case_link = request.POST.get('case_link')
        user.save()
        return redirect_params('cases',{'user':user})

    return render(request,'backboard/cases.html',{'user':user})

def faq(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/')
    
    if request.GET.get('delete_id') != None:
      FAQ.objects.get(id=request.GET.get('delete_id')).delete()

    faqs = FAQ.objects.all().order_by('-id')

    paginator = Paginator(faqs, 20)
    if request.GET.get('page') != None:
        page_number = request.GET.get('page') 
    else:
        page_number = 1
    page_obj = paginator.get_page(page_number)

    page_obj.adjusted_elided_pages = paginator.get_elided_page_range(page_number)
   
    return render(request,'backboard/faq.html', {'faqs':page_obj})

def new_edit_faq(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/')
    
    if request.method == 'POST':
        
        if request.GET.get('faq_id') != None:
            faq = FAQ.objects.get(id=request.GET.get('faq_id'))
        else:
            faq = FAQ()
            faq.create_date = datetime.datetime.now()

        faq.title = request.POST.get('title') 
        faq.body = request.POST.get('body') 
        faq.user = request.user
        faq.save()

        return redirect_params('faq',{'faq':faq})
    
    if request.GET.get('faq_id') != None:
        faq = FAQ.objects.get(id=request.GET.get('faq_id'))
        return render(request, 'backboard/new_edit_faq.html', {'faq':faq})

    return render(request,'backboard/new_edit_faq.html')

def advert_setting(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/')
    
    user = request.user
    if request.method == 'POST':
        user.fb_pixel = request.POST.get('fb_pixel')
        user.google_id = request.POST.get('google_id')
        user.save()
        return redirect_params('advert_setting',{'user':user})

    return render(request,'backboard/advert_setting.html',{'user':user})

def bills(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/')
    
    return render(request,'backboard/bills.html')

def setting(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/')
    
    user = request.user
    return render(request,'backboard/setting.html',{'user':user})

def redirect_params(url, params=None):
    
    response = redirect(url)
    if params:
        query_string = urllib.parse.urlencode(params)
        response['Location'] += '?' + query_string
    return response