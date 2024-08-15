from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Member, Product, checkoutitem, CartItem, userorder, forcontact
from django.core.mail import send_mail

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

def about(request):
    return render(request, 'about.html')

def cart(request):
    return render(request,'cart.html')

def checkout(request):
    if request.method == 'POST':
        country = request.POST['country']
        fname = request.POST['fname']
        lname = request.POST['lname']
        C_address= request.POST['C_address'] 
        state= request.POST['state']
        zip = request.POST['zip']
        emailADD = request.POST['emailADD']
        phoneNO= request.POST['phoneNO'] 
        
        y = checkoutitem(country=country,fname=fname,lname=lname,C_address=C_address,state=state,zip=zip,emailADD=emailADD,phoneNO=phoneNO)
        y.save()
        return redirect("thankyou")
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'checkout.html', {'cart_items': cart_items, 'total_price': total_price })

def contact(request):
    if request.method == 'POST':
        f_name = request.POST['f_name']
        l_name = request.POST['l_name']
        c_email = request.POST['c_email']
        message= request.POST['message'] 
        z = forcontact(f_name=f_name,l_name=l_name,c_email=c_email,message=message)
        z.save()
    return render(request,'contact.html')


def shop(request):
    return render(request,'shop.html')

def thankyou(request):
    return render(request,'thankyou.html')

def profile(request):
    username = request.session.get('username')
    data = Member.objects.filter(username=username)
    d = {'username' :data}
    return render(request,'profile.html' , d)

def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop.html', {'products': products})
 
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price })
 
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(product=product, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('product_list')
 
def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.delete()
    return redirect('view_cart')

def send_email(request):
    subject = 'testing email'
    message = 'thanks.'
    email_from = 'kachhadiyagd@gmail.com'
    recipient_list = ['jaydesai2304@gmail.com']

    send_mail(subject, message, email_from, recipient_list)
    return redirect('login')

def buy_now(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(product=product, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('checkout')

def placeorder(request):
    product = CartItem.objects.get()
    cart_item, created = userorder.objects.get_or_create(product=product )
    cart_item.quantity += 1
    cart_item.save()
    return redirect('thankyou')


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

def logout(request):
    try:
        del request.session['email']
        del request.session['username']
        return render(request,'login.html')
    except:
        return render(request,'login.html')
