from django.shortcuts import render
from django.http import HttpResponse
from .ecpay_test import main
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger(__file__)

@csrf_exempt
def ecpay_view(request):
    return HttpResponse(main())

@csrf_exempt
def ecpay_callback(request):
    logger.info(request.body.decode('utf-8'))
    return HttpResponse('1|OK')
