from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Product, CartItem, ShippingAddress, Order, OrderItem, ContactMessage, WishlistItem, Review
from django.core.mail import send_mail
from django.db.models import Q

def index(request):
    featured_products = Product.objects.all()[:3]
    return render(request, 'index.html', {'products': featured_products})

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        f_name = request.POST.get('f_name')
        l_name = request.POST.get('l_name')
        c_email = request.POST.get('c_email')
        message = request.POST.get('message')
        ContactMessage.objects.create(f_name=f_name, l_name=l_name, c_email=c_email, message=message)
        messages.success(request, "Your message has been sent successfully!")
        return redirect('contact')
    return render(request, 'contact.html')

def shop(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    else:
        products = Product.objects.all()
    return render(request, 'shop.html', {'products': products, 'query': query})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.all().order_by('-created_at')
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to leave a review.")
            return redirect('login')
        
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        if rating and comment:
            Review.objects.create(
                product=product,
                user=request.user,
                rating=rating,
                comment=comment
            )
            messages.success(request, "Thank you for your review!")
            return redirect('product_detail', product_id=product.id)

    return render(request, 'product_detail.html', {'product': product, 'reviews': reviews})

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password'] 
        confirm_password = request.POST['confirm_password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect("register")
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("register")
        
        user = User.objects.create_user(username=username, email=email, password=password)
        auth_login(request, user)
        messages.success(request, f"Welcome {username}! Your account has been created.")
        return redirect("index")
        
    return render(request, 'register.html')

def Login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password")
            return render(request, 'login.html')
    return render(request, 'login.html')

def logout(request):
    auth_logout(request)
    return redirect('login')

@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.total_price for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(product=product, user=request.user)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    else:
        cart_item.quantity = 1
        cart_item.save()
    messages.success(request, f"{product.name} added to cart.")
    return redirect('view_cart')

@login_required
def update_cart_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    action = request.POST.get('action')
    if action == 'increase':
        cart_item.quantity += 1
        cart_item.save()
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    return redirect('view_cart')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    return redirect('view_cart')

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items:
        return redirect('product_list')
    
    total_price = sum(item.total_price for item in cart_items)
    
    if request.method == 'POST':
        # Create Shipping Address
        address = ShippingAddress.objects.create(
            user=request.user,
            country=request.POST.get('country'),
            fname=request.POST.get('fname'),
            lname=request.POST.get('lname'),
            address=request.POST.get('C_address'),
            state=request.POST.get('state'),
            zip_code=request.POST.get('zip'),
            email=request.POST.get('emailADD'),
            phone=request.POST.get('phoneNO')
        )
        
        # Create Order
        order = Order.objects.create(
            user=request.user,
            shipping_address=address,
            total_amount=total_price
        )
        
        # Create Order Items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
        
        # Clear Cart
        cart_items.delete()
        
        return redirect('thankyou')

    return render(request, 'checkout.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order_history.html', {'orders': orders})

def thankyou(request):
    return render(request, 'thankyou.html')

def buy_now(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(product=product, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('checkout')

def send_email(request):
    # This remains as requested but should be updated with real logic if needed
    subject = 'testing email'
    message = 'thanks.'
    email_from = 'kachhadiyagd@gmail.com'
    recipient_list = ['jaydesai2304@gmail.com']
    send_mail(subject, message, email_from, recipient_list)
    return redirect('login')

@login_required
def view_wishlist(request):
    wishlist_items = WishlistItem.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    WishlistItem.objects.get_or_create(user=request.user, product=product)
    messages.success(request, f"{product.name} added to wishlist.")
    return redirect('product_list')

@login_required
def remove_from_wishlist(request, item_id):
    wishlist_item = get_object_or_404(WishlistItem, id=item_id, user=request.user)
    wishlist_item.delete()
    return redirect('view_wishlist')

