from django.contrib import admin

from django.contrib import admin
from .models import Member


class Admin(admin.ModelAdmin):
    list_display=("username", "email","phone")
    

admin.site.register(Member, Admin)

