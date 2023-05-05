from django.shortcuts import render
from django.http import HttpResponse
from .ecpay_test import main
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def ecpay_view(request):
    return HttpResponse(main())

