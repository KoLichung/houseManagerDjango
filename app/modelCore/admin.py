from django.contrib import admin
from .models import User, HouseCase


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'company', 'serve_place', 'email')
    search_fields = ['serve_place','name']

@admin.register(HouseCase)
class HouseCaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'type')