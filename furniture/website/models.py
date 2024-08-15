from django.db import models
from django.contrib.auth.models import User

class Member(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length = 100)
    phone = models.CharField(max_length =100)
    password = models.CharField(max_length=100)
    confirm_password=models.CharField(max_length=100)