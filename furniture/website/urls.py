from django.urls import path
from website import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name="index"),
    path('register/', views.register, name="register"),
    path('login/', views.Login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),
    path('thankyou/', views.thankyou, name="thankyou"),
    path('shop/', views.shop, name="product_list"),
    path('product/<int:product_id>/', views.product_detail, name="product_detail"),
    path('cart/', views.view_cart, name='view_cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart/<int:item_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('checkout/', views.checkout, name="checkout"),
    path('orders/', views.order_history, name="order_history"),
    path('send-email/', views.send_email, name='send_email'),
    path("buy/<int:product_id>/", views.buy_now, name="buy_now" ),
    path('wishlist/', views.view_wishlist, name='view_wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:item_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
]


if settings.DEBUG:  
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)