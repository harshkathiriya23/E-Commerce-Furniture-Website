from django.urls import path
from website import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name="index"),
    path('register/', views.register, name="register"),
    path('login/', views.Login, name="login"),
    path('about/', views.about, name="about"),
    path('checkout/', views.checkout, name="checkout"),
    path('contact/', views.contact, name="contact"),
    path('thankyou/', views.thankyou, name="thankyou"),
    path('profile/', views.profile, name="profile"),
    path('shop/', views.product_list, name="product_list"),
    path('cart/', views.view_cart, name='view_cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('send-email/', views.send_email, name='send_email'),
    path("buy/<int:product_id>/", views.buy_now, name="buy_now" ),
    path("placeorder/", views.placeorder, name="placeorder" ),
    path('logout/', views.logout, name="logout"),
]

if settings.DEBUG:  
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)