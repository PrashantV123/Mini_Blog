from atexit import register
from django.contrib import admin
from .models import Contact, post

# Register your models here.


@admin.register(post)
class postModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title', 'desc']


@admin.register(Contact)
class ContactUSModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'address', 'message']
