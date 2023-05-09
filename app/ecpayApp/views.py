from django.shortcuts import render
from django.http import HttpResponse
from .ecpay_test import main
from django.views.decorators.csrf import csrf_exempt
from modelCore.models import Order, User
import logging
import json
from urllib import parse
from datetime import datetime
from dateutil.relativedelta import relativedelta

logger = logging.getLogger(__file__)

@csrf_exempt
def ecpay_view(request):
    return HttpResponse(main())

@csrf_exempt
def ecpay_callback(request):
    data = request.body.decode('utf-8')
    data_json = dict(parse.parse_qsl(parse.urlsplit(data).path))
    
    logger.info(data_json)

    order = Order()
    order.amount = data_json.get('amount', 0)
    order.auth_code = data_json.get('auth_code', '')
    order.card4no = data_json.get('card4no', '')
    order.card6no = data_json.get('card6no', '')
    order.CustomField1 = data_json.get('CustomField1', '')
    order.ExecTimes = data_json.get('ExecTimes', 0)
    order.Frequency = data_json.get('Frequency', 0)
    order.gwsr = data_json.get('gwsr', '')
    order.MerchantID = data_json.get('MerchantID', '')
    order.MerchantTradeNo = data_json.get('MerchantTradeNo', '')
    order.PaymentDate = data_json.get('PaymentDate', '')
    order.PaymentType = data_json.get('PaymentType', '')
    order.PaymentTypeChargeFee = data_json.get('PaymentTypeChargeFee', '')

    order.PeriodAmount = data_json.get('PeriodAmount', 0)
    order.PeriodType = data_json.get('PeriodType', '')
    
    order.process_date = data_json.get('process_date', '')
    order.RtnCode = data_json.get('RtnCode', '')
    order.RtnMsg = data_json.get('RtnMsg', '')
    order.SimulatePaid = data_json.get('SimulatePaid', '')
    order.TotalSuccessAmount = data_json.get('TotalSuccessAmount', 0)
    order.TotalSuccessTimes = data_json.get('TotalSuccessTimes', 0)
    order.TradeAmt = data_json.get('TradeAmt', 0)
    order.TradeDate = data_json.get('TradeDate', '')
    order.TradeNo = data_json.get('TradeNo', '')
    order.CheckMacValue = data_json.get('CheckMacValue', '')

    user_id = int(order.CustomField1)
    order.user = User.objects.get(id=user_id)
    
    if order.RtnCode == '1':
        order.state = 'PAID'
    else:
        order.state = 'UNPAID'
    
    order.price = order.amount
    order.time_period = 1

    order.pay_date = datetime.strptime(order.PaymentDate, '%Y/%m/%d %H:%M:%S')

    if Order.objects.filter(user=order.user,state='PAID').count() != 0 and Order.objects.filter(user=order.user,state='PAID').order_by('-id').first().expire_date > datetime.now():
        last_order = Order.objects.filter(user=order.user,state='PAID').order_by('-id').first()
        if order.PeriodType == 'M':
            order.expire_date = last_order.expire_date + relativedelta(months=1)
            order.plan = 'monthly'
        else:
            order.expire_date = last_order.expire_date + relativedelta(years=1)
            order.plan = 'yearly'
    else:
        start_date_time = datetime.now()
        if order.PeriodType == 'M':
            order.expire_date = start_date_time + relativedelta(months=1)
            order.plan = 'monthly'
        else:
            order.expire_date = start_date_time + relativedelta(years=1)
            order.plan = 'yearly'
    
    order.save()

    return HttpResponse('1|OK')
