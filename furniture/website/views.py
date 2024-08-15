from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Member

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        password= request.POST['password'] 
        confirm_password= request.POST['confirm_password']

        if Member.objects.filter(username=username).exists():
            messages.error(request,"username already taken")
            return redirect("register")
        
        if password != confirm_password:
            messages.error(request,"password doesn't match")
            return redirect("register")
        x = Member(username = username,email=email,phone=phone, password=password, confirm_password=confirm_password)
        x.save()
        return redirect("login")
        
    return render(request, 'register.html')

def Login(request):
    if request.method=="POST":
        try:
            user=Member.objects.get(
                username=request.POST['username'],
                password=request.POST['password'],
            )
            request.session['email']=user.email
            request.session['username']=user.username
            return render(request,'index.html')
        except:

            return render(request,'login.html')
    else:
        return render(request,'login.html')
    
def index(request):
    return render(request, 'index.html' ,{"nbar": index})