from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.http import HttpResponse
from modelCore.models import User, FAQ, HouseCase, Order, Coupon
import urllib
import datetime
from modelCore.forms import AboutForm, TestimonialForm, UserMainImageForm, UserAvatarForm
from django.contrib import auth
from django.contrib.auth import authenticate

from ecpayApp.ecpay_test import main
from django.views.decorators.csrf import csrf_exempt

from django.utils import timezone

# Create your views here.

def logout(request):
    auth.logout(request)
    return redirect('/')

def top_video(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    
    user = request.user
    if request.method == 'POST':

        user.video_link = request.POST.get('video_link')
        user.video_bg_color = request.POST.get('bg_color')
        
        # if 'v=' in user.video_link:
        #     index = user.video_link.index('v=')
        #     video_id = user.video_link[index+2:]
        #     user.video_id = video_id
        
        # Examples:
        # - http://youtu.be/SA2iWivDJiE
        # - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
        # - http://www.youtube.com/embed/SA2iWivDJiE
        # - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US

        query = urllib.parse.urlparse(user.video_link)
        if query.hostname == 'youtu.be':
            user.video_id =  query.path[1:]
        if query.hostname in ('www.youtube.com', 'youtube.com'):
            if query.path == '/watch':
                p = urllib.parse.parse_qs(query.query)
                user.video_id = p['v'][0]
            if query.path[:7] == '/embed/':
                user.video_id  = query.path.split('/')[2]
            if query.path[:3] == '/v/':
                user.video_id = query.path.split('/')[2]

        user.video_title = request.POST.get('video_title')
        user.video_subtitle = request.POST.get('video_subtitle')
        user.save()
        
        return redirect_params('top_video',{'user':user})

    return render(request,'backboard/top_video.html',{'user':user})

def main_image(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    
    user = request.user 
    if request.method == 'POST':
        if request.FILES.get('main_image', False):
            user.main_image = request.FILES['main_image']
        user.save()

    if request.GET.get('main_image') != None:
        form = UserMainImageForm(instance=user)
        return render(request, 'backboard/main_image.html', {'form':form})

    form = UserMainImageForm()
    return render(request,'backboard/main_image.html',{'user':user,'form':form})

def about(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    user = request.user

    if request.method == 'POST':
        if request.FILES.get('avatar', False):
            user.avatar = request.FILES['avatar']
            user.save()
    
    if request.method == 'POST' and 'nickname' in request.POST:
        user.nickname = request.POST.get('nickname')
        user.phone_number = request.POST.get('phone_number')

        if request.POST.get('line_id') != None:
            user.line_id = request.POST.get('line_id')
        else:
            user.line_id = ''

        user.about_me = request.POST.get('about_me')
        user.save()  
        return redirect_params('about',{'user':user})
    
    form = AboutForm(instance=user)
    avatar_form = UserAvatarForm()

    return render(request,'backboard/about.html',{'user':user, 'form':form, 'avatar_form':avatar_form})

def testimonial(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    user = request.user
    if request.method == 'POST':
        user.testimonial = request.POST.get('testimonial')
        user.save()  
        return redirect_params('testimonial',{'user':user})

    form = TestimonialForm(instance=user)
    return render(request,'backboard/testimonial.html',{'user':user,'form':form} )

def cases(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    user = request.user
    if request.method == 'POST':
        user.case_link = request.POST.get('case_link')
        user.save()
        
        HouseCase.objects.filter(user=user).delete()

        from seleniumApp.tasks import crawl_manager_cases_by_requests
        crawl_manager_cases_by_requests(user, user.case_link)

        return redirect_params('cases',{'user':user})

    cases = HouseCase.objects.filter(user=user)

    return render(request,'backboard/cases.html',{'user':user, 'cases':cases})

def faq(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    
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
    if not request.user.is_authenticated:
        return redirect('/login')
    
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
    if not request.user.is_authenticated:
        return redirect('/login')
    
    user = request.user
    if request.method == 'POST':
        user.fb_pixel = request.POST.get('fb_pixel')
        user.google_id = request.POST.get('google_id')
        user.save()
        return redirect_params('advert_setting',{'user':user})

    return render(request,'backboard/advert_setting.html',{'user':user})

def bills(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    
    user = request.user
    orders = Order.objects.filter(user=user,state='PAID')
    
    return render(request,'backboard/bills.html', {'orders':orders})

def plans(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    return render(request,'backboard/plans.html')

def upgrade(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    
    plan = request.GET.get('plan')
    if plan != None:
        if plan == 'yearly':
            amount = 4500
        if plan == 'monthly':
            amount = 499
    else:
        return redirect('plans')

    message = ''

    if request.GET.get('coupon') != None:
        coupon_code = request.GET.get('coupon')
        if Coupon.objects.filter(code=coupon_code).count()!=0:
            coupon = Coupon.objects.filter(code=coupon_code).first()

            year = coupon.expire_date.year
            month = coupon.expire_date.month
            day = coupon.expire_date.day
            hour = coupon.expire_date.hour
            minute = coupon.expire_date.minute
            second = coupon.expire_date.second
            new_expire_date = datetime.datetime(year, month, day, hour, minute, second)

            if new_expire_date > datetime.datetime.now():
                coupon_percent = coupon.count_percent
                amount = int(amount*coupon_percent/100)
                if plan == 'yearly':
                    message=f'您使用了折價券！折價後金額為 <span style="color: red;">${amount}</span> / 年!'
                else:
                    message=f'您使用了折價券！折價後金額為 {amount} / 月!'
            else:
                message=f'折價券過期了!'
        else:
            message='找不到此 Coupon 折價券~'
    
    return render(request,'backboard/upgrade.html',{'plan':plan,'message':message,'amount':amount})

def payment(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    
    user = request.user.id
    plan = request.GET.get('plan')
    amount = request.GET.get('amount')

    if plan == None or amount == None:
        return redirect('plans')

    # return render(request,'backboard/payment.html')
    return redirect_params('ecpayApp:ecpay',{'user':user, 'plan':plan,'amount':amount})


def setting(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    
    user = request.user
    if request.method == 'POST' and 'reset_password' in request.POST:
        password = request.POST.get('password')
        user.set_password(password)
        user.save()
        return redirect_params('setting',{'user':user})

    return render(request,'backboard/setting.html',{'user':user})



# ===========================================

def redirect_params(url, params=None):
    response = redirect(url)
    if params:
        query_string = urllib.parse.urlencode(params)
        response['Location'] += '?' + query_string
    return response