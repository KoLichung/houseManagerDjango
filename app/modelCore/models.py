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
    name = models.CharField(max_length=255, default='', blank=True, null=True, unique=True)
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

    about_me = RichTextUploadingField(config_name='about_me', default='')
    
    #親友見證
    testimonial = RichTextUploadingField(config_name='testimonial', default='')
    
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

class Bills(models.Model):
    user =  models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
    )
    #繳款金額			
    price = models.IntegerField(default=0)
    #服務時長
    duration = models.IntegerField(default=0)
    #繳款日
    pay_date = models.DateField(null=True)
    #實際到期日
    expire_date = models.DateField(null=True)

