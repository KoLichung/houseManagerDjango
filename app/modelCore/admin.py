from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'company', 'serve_place', 'email')
    search_fields = ['serve_place','name']