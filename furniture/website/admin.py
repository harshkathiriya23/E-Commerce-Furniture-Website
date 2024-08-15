from django.contrib import admin

from django.contrib import admin
from .models import Member, Product, CartItem, checkoutitem, forcontact,userorder


class Admin(admin.ModelAdmin):
    list_display=("username", "email","phone")
    
class cheoutdetail(admin.ModelAdmin):
    list_display=("country","fname","C_address","state","zip","phoneNO")
    
class message_user(admin.ModelAdmin):
    list_display=("f_name","c_email","message")
    

admin.site.register(Member, Admin)
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(checkoutitem,cheoutdetail)
admin.site.register(forcontact,message_user)
admin.site.register(userorder)
