from django.db import models
from django.contrib.auth.models import User

class Member(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length = 100)
    phone = models.CharField(max_length =100)
    password = models.CharField(max_length=100)
    confirm_password=models.CharField(max_length=100)

class Product(models.Model):
    name = models.CharField(max_length=100)
    discription = models.CharField(max_length=100,default='')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
 
    def __str__(self):
        return self.name
 
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return f'{self.quantity} x {self.product.name}'
    
class checkoutitem(models.Model):
    country = models.CharField(max_length=100,default='')
    fname = models.CharField(max_length = 100,default='')
    lname = models.CharField(max_length =100,default='')
    C_address = models.CharField(max_length=255 , default='')
    state = models.CharField(max_length=100,default='')
    zip = models.CharField(max_length=100,default='')
    emailADD = models.EmailField(max_length = 100,default='')
    phoneNO = models.CharField(max_length =10,default='')


    
class forcontact(models.Model):
    f_name = models.CharField(max_length=100,default='')
    l_name = models.CharField(max_length = 100,default='')
    c_email = models.EmailField(max_length =100,default='')
    message = models.CharField(max_length=255 , default='')
    
class userorder(models.Model):
    product = models.ForeignKey(CartItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)