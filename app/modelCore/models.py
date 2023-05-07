import pathlib
import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField

def image_upload_handler(instance,filename):
    fpath = pathlib.Path(filename)
    new_fname = str(uuid.uuid1()) #uuid1 -> uuid + timestamp
    return f'images/{new_fname}{fpath.suffix}'

@property
def get_photo_url(self):
    if self.photo and hasattr(self.photo, 'url'):
        return self.photo.url
    else:
        return "/static/web/assets/img/generic/2.jpg"

class UserManager(BaseUserManager):

    def create_user(self, phone, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not phone:
            raise ValueError('Users must have an phone')
        # user = self.model(email=self.normalize_email(email), **extra_fields)
        user = self.model(
            phone = phone, 
            name=extra_fields.get('name'),
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, phone, password, **extra_fields):
        """Creates and saves a new super user"""
        user = self.create_user(phone, password, **extra_fields)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that suppors using email instead of username"""
    phone = models.CharField(max_length=10, unique=True, blank=True, null=True)
    name = models.CharField(max_length=255, default='', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    is_passed = models.BooleanField(default=False)

    objects = UserManager()

    company = models.CharField(max_length=255, default='', blank=True, null=True)
    serve_place = models.CharField(max_length=255, default='', blank=True, null=True)
    serve_time = models.CharField(max_length=255, default='', blank=True, null=True)
    email = models.CharField(max_length=255, default='', blank=True, null=True)

    familiar_complex = models.CharField(max_length=255, default='', blank=True, null=True)
    good_at = models.CharField(max_length=255, default='', blank=True, null=True)

    page_link = models.CharField(max_length=255, default='', blank=True, null=True)

    USERNAME_FIELD = 'phone'

    #置頂影片
    video_link = models.CharField(max_length=255, default='', blank=True, null=True)
    video_id = models.CharField(max_length=30, default='', blank=True, null=True)

    video_title = models.CharField(max_length=255, default='', blank=True, null=True)
    video_subtitle = models.CharField(max_length=255, default='', blank=True, null=True)

    #主圖
    main_image = models.ImageField(upload_to=image_upload_handler, blank=True, null=True)

    #關於我
    avatar = models.ImageField(upload_to=image_upload_handler, blank=True, null=True)
    nickname = models.CharField(max_length=10, default='', blank=True, null=True)
    phone_number = models.CharField(max_length=10, unique=True, blank=True, null=True)
    line_id  = models.CharField(max_length=10, unique=True, blank=True, null=True)

    about_me = RichTextUploadingField(config_name='about_me', default='', blank=True, null=True)
    
    #親友見證
    testimonial = RichTextUploadingField(config_name='testimonial', default='', blank=True, null=True)
    
    #591連結
    case_link = models.CharField(max_length=255, default='', blank=True, null=True)
    
    #廣告追蹤設定
    fb_pixel  = models.CharField(max_length=30, unique=True, blank=True, null=True)
    google_id  = models.CharField(max_length=30, unique=True, blank=True, null=True)
 
class HouseCase(models.Model):
    user =  models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
    )
    title = models.CharField(max_length=100, default='', blank = True, null=True)
    address = models.CharField(max_length=20, default='', blank = True, null=True)
    #3房2廳、店面、土地
    type = models.CharField(max_length=20, default='', blank = True, null=True)
    #坪數
    units = models.CharField(max_length=20, default='', blank = True, null=True)
    price = models.CharField(max_length=20, default='', blank = True, null=True)
    #圖片連結
    image = models.CharField(max_length=255, default='', blank = True, null=True)
    case_link = models.CharField(max_length=255, default='', blank = True, null=True)
    shop_id = models.CharField(max_length=20, default='', blank = True, null=True)

class FAQ(models.Model):
    user =  models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
    )

    title = models.CharField(max_length = 255, blank = True, null=True)
    body = models.TextField(default='', blank = True, null=True)
    create_date = models.DateField(blank = True, null=True)

class Order(models.Model):
    user =  models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
    )
    
    STATE_CHOICES = [
        ('UNPAID', '未付款'),
        ('PAID', '已付款'),
    ]
    state =  models.CharField(max_length=20, choices=STATE_CHOICES,default='UNPAID')

    #繳款金額			
    price = models.IntegerField(default=0)
    
    #服務時長
    time_period = models.IntegerField(default=0)

    #繳款日
    pay_date = models.DateField(null=True)
    
    #實際到期日
    expire_date = models.DateField(null=True)
    
    #選擇方案 monthly, yearly
    plan = models.CharField(max_length=10, default='', blank = True, null=True)
    
    # ====== 以下為綠界回傳欄位
    amount = models.IntegerField(default=0)
    auth_code = models.CharField(max_length=25, default='', blank = True, null=True)
    card4no = models.CharField(max_length=25, default='', blank = True, null=True)
    card6no = models.CharField(max_length=25, default='', blank = True, null=True)
    CustomField1 = models.CharField(max_length=25, default='', blank = True, null=True)
    ExecTimes = models.IntegerField(default=0)
    Frequency = models.IntegerField(default=0)
    gwsr = models.CharField(max_length=25, default='', blank = True, null=True)
    MerchantID = models.CharField(max_length=25, default='', blank = True, null=True)
    MerchantTradeNo = models.CharField(max_length=30, default='', blank = True, null=True)

    PaymentDate = models.CharField(max_length=30, default='', blank = True, null=True)
    PaymentType = models.CharField(max_length=30, default='', blank = True, null=True)
    PaymentTypeChargeFee = models.CharField(max_length=20, default='', blank = True, null=True)

    PeriodAmount = models.IntegerField(default=0)
    PeriodType = models.CharField(max_length=10, default='', blank = True, null=True)
    process_date = models.CharField(max_length=30, default='', blank = True, null=True)
    RtnCode = models.CharField(max_length=10, default='', blank = True, null=True)
    RtnMsg = models.CharField(max_length=30, default='', blank = True, null=True)

    SimulatePaid = models.CharField(max_length=10, default='', blank = True, null=True)
    TotalSuccessAmount = models.IntegerField(default=0)
    TotalSuccessTimes = models.IntegerField(default=0)
    TradeAmt = models.IntegerField(default=0)
    TradeDate = models.CharField(max_length=30, default='', blank = True, null=True)
    TradeNo = models.CharField(max_length=50, default='', blank = True, null=True) #可能會有多次回傳,但這個欄位應該是唯一的
    CheckMacValue = models.CharField(max_length=125, default='', blank = True, null=True)


# class Payment(models.Model):

#     order = models.ForeignKey(
#         Order,
#         on_delete=models.RESTRICT,
#         default=''
#     )

#     # {"amount": "2000", 
#     # "auth_code": "777777", 
#     # "card4no": "2222", 
#     # "card6no": "431195", 
#     # "CustomField1": "4"
#     # "ExecTimes": "99", 
#     # "Frequency": "1", 
#     # "gwsr": "12609859", 
#     # "MerchantID": "3002599", 
#     # "MerchantTradeNo": "NO20230506085721", 
#     # "PaymentDate": "2023/05/06 16:57:53", 
#     # "PaymentType": "Credit_CreditCard", 
#     # "PaymentTypeChargeFee": "49", 
#     # "PeriodAmount": "2000", 
#     # "PeriodType": "M", 
#     # "process_date": "2023/05/06 16:57:53", 
#     # "RtnCode": "1", 
#     # "RtnMsg": "交易成功", 
#     # "SimulatePaid": "0", 
#     # "TotalSuccessAmount": "2000", 
#     # "TotalSuccessTimes": "1", 
#     # "TradeAmt": "2000", 
#     # "TradeDate": "2023/05/06 16:57:21", 
#     # "TradeNo": "2305061657216063", 
#     # "CheckMacValue": "ACFBFD1183BF53574F3B13D41D9C7D098CF04355755287D2032E0145DBDE6783"}

#     # ====== 以下為綠界回傳欄位
#     amount = models.IntegerField(default=0)
#     auth_code = models.CharField(max_length=25, default='', blank = True, null=True)
#     card4no = models.CharField(max_length=25, default='', blank = True, null=True)
#     card6no = models.CharField(max_length=25, default='', blank = True, null=True)
#     CustomField1 = models.CharField(max_length=25, default='', blank = True, null=True)
#     ExecTimes = models.IntegerField(default=0)
#     Frequency = models.IntegerField(default=0)
#     gwsr = models.CharField(max_length=25, default='', blank = True, null=True)
#     MerchantID = models.CharField(max_length=25, default='', blank = True, null=True)
#     MerchantTradeNo = models.CharField(max_length=30, default='', blank = True, null=True)

#     PaymentDate = models.CharField(max_length=30, default='', blank = True, null=True)
#     PaymentType = models.CharField(max_length=30, default='', blank = True, null=True)
#     PaymentTypeChargeFee = models.CharField(max_length=20, default='', blank = True, null=True)

#     PeriodAmount = models.IntegerField(default=0)
#     PeriodType = models.CharField(max_length=10, default='', blank = True, null=True)
#     process_date = models.CharField(max_length=30, default='', blank = True, null=True)
#     RtnCode = models.CharField(max_length=10, default='', blank = True, null=True)
#     RtnMsg = models.CharField(max_length=30, default='', blank = True, null=True)

#     SimulatePaid = models.CharField(max_length=10, default='', blank = True, null=True)
#     TotalSuccessAmount = models.IntegerField(default=0)
#     TotalSuccessTimes = models.IntegerField(default=0)
#     TradeAmt = models.IntegerField(default=0)
#     TradeDate = models.CharField(max_length=30, default='', blank = True, null=True)
#     TradeNo = models.CharField(max_length=50, default='', blank = True, null=True)
#     CheckMacValue = models.CharField(max_length=125, default='', blank = True, null=True)

    



