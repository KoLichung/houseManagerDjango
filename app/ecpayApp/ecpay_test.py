from django.test import TestCase

import importlib.util
spec = importlib.util.spec_from_file_location(
    "ecpay_payment_sdk",
    "ecpayApp/ecpay_payment_sdk.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
from datetime import datetime

def main():

    order_params = {
        'MerchantTradeNo': datetime.now().strftime("NO%Y%m%d%H%M%S"),
        'StoreID': '',
        'MerchantTradeDate': datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
        'PaymentType': 'aio',
        'TotalAmount': 2000, #商品金額
        'TradeDesc': '訂單測試', #交易描述
        'ItemName': '商品1#商品2', #商品名稱，用井字號當分行 
        
        # 付款完成通知回傳網址
        'ReturnURL': 'https://www.ecpay.com.tw/return_url.php', 

        'ChoosePayment': 'Credit', # 顧客的付費方式

        # 結帳後，先導到 OrderResultURL，從綠界頁面跳回的頁面
        # 如果沒有參數才會跳轉到 ClientBackURL
        'ClientBackURL': 'https://www.ecpay.com.tw/client_back_url.php',
        'ItemURL': 'https://www.ecpay.com.tw/item_url.php', # 商品資訊頁面
        'Remark': '交易備註',
        'ChooseSubPayment': '',
        
        # 結帳成功/失敗後的結果頁面，告知顧客本次的結帳結果
        'OrderResultURL': 'https://www.ecpay.com.tw/order_result_url.php',
        'NeedExtraPaidInfo': 'Y',
        'DeviceSource': '',
        'IgnorePayment': '',
        'PlatformID': '',
        'InvoiceMark': 'N',
        'CustomField1': '',
        'CustomField2': '',
        'CustomField3': '',
        'CustomField4': '',
        'EncryptType': 1,
    }

    extend_params_1 = {
        'BindingCard': 0,
        'MerchantMemberID': '',
    }

    extend_params_2 = {
        'Language': '',
    }

    # 發票資訊
    inv_params = {
        # 'RelateNumber': 'Tea0001', # 特店自訂編號
        # 'CustomerID': 'TEA_0000001', # 客戶編號
        # 'CustomerIdentifier': '53348111', # 統一編號
        # 'CustomerName': '客戶名稱',
        # 'CustomerAddr': '客戶地址',
        # 'CustomerPhone': '0912345678', # 客戶手機號碼
        # 'CustomerEmail': 'abc@ecpay.com.tw',
        # 'ClearanceMark': '2', # 通關方式
        # 'TaxType': '1', # 課稅類別
        # 'CarruerType': '', # 載具類別
        # 'CarruerNum': '', # 載具編號
        # 'Donation': '1', # 捐贈註記
        # 'LoveCode': '168001', # 捐贈碼
        # 'Print': '1',
        # 'InvoiceItemName': '測試商品1|測試商品2',
        # 'InvoiceItemCount': '2|3',
        # 'InvoiceItemWord': '個|包',
        # 'InvoiceItemPrice': '35|10',
        # 'InvoiceItemTaxType': '1|1',
        # 'InvoiceRemark': '測試商品1的說明|測試商品2的說明',
        # 'DelayDay': '0', # 延遲天數
        # 'InvType': '07', # 字軌類別
    }

    # 定期定額相關參數
    period_params = {
        'PeriodAmount': 2000, # 交易金額[TotalAmount]設定金額必須和授權金額[PeriodAmount]相同。
        'PeriodType': 'M',
        'Frequency': '1',
        'ExecTimes': '2',
        'PeriodReturnURL': 'https://www.ecpay.com.tw/receive.php'
    }

    # 建立實體
    ecpay_payment_sdk = module.ECPayPaymentSdk(
        MerchantID='3002599',
        HashKey='spPjZn66i0OhqJsQ',
        HashIV='hT5OJckN45isQTTs'
    )

    # 合併延伸參數
    order_params.update(extend_params_1)
    order_params.update(extend_params_2)

    # 合併發票參數
    order_params.update(inv_params)

    # 合併定期定額參數
    order_params.update(period_params)

    try:
        # 產生綠界訂單所需參數
        final_order_params = ecpay_payment_sdk.create_order(order_params)

        # 產生 html 的 form 格式
        action_url = 'https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5'  # 測試環境
        # action_url = 'https://payment.ecpay.com.tw/Cashier/AioCheckOut/V5' # 正式環境
        html = ecpay_payment_sdk.gen_html_post_form(action_url, final_order_params)
        print(html)
        return html
    except Exception as error:
        print('An exception happened: ' + str(error))