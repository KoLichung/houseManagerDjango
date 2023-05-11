from django.contrib import admin
from .models import User, HouseCase, Order, Coupon


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','nickname','name','phone','company','serve_place','email')
    search_fields = ['serve_place','name','nickname']

@admin.register(HouseCase)
class HouseCaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'type')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'state', 'price', 'pay_date', 'expire_date')

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'count_percent', 'expire_date')