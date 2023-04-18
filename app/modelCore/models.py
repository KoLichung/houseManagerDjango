from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.urls import reverse

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

    objects = UserManager()

    company = models.CharField(max_length=255, default='', blank=True, null=True)
    serve_place = models.CharField(max_length=255, default='', blank=True, null=True)
    serve_time = models.CharField(max_length=255, default='', blank=True, null=True)
    email = models.CharField(max_length=255, default='', blank=True, null=True)

    familiar_complex = models.CharField(max_length=255, default='', blank=True, null=True)
    good_at = models.CharField(max_length=255, default='', blank=True, null=True)

    page_link = models.CharField(max_length=255, default='', blank=True, null=True)

    USERNAME_FIELD = 'name'
    
class HouseCase(models.Model):
    title = models.CharField(max_length=100, default='', blank = True, null=True)
    address = models.CharField(max_length=20, default='', blank = True, null=True)
    #3房2廳、店面、土地
    type = models.CharField(max_length=20, default='', blank = True, null=True)
    #坪數
    units = models.CharField(max_length=20, default='', blank = True, null=True)
    price = models.CharField(max_length=20, default='', blank = True, null=True)
    #圖片連結
    image = models.CharField(max_length=255, default='', blank = True, null=True)

class FAQ(models.Model):
    user =  models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
    )