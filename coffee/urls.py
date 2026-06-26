from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.conf import settings                   
from django.conf.urls.static import static 


urlpatterns = [
    path('', views.cover_page, name='cover'),  # Cover page first
    path('shop/', views.home, name='home'),
    path('add/', views.add_coffee, name='add_coffee'),
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:coffee_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/<int:item_id>/', views.update_cart, name='update_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    #path('login/', auth_views.LoginView.as_view(template_name='shop/login.html'), name='login'),
    path('login/', views.custom_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/',views.custom_logout, name='logout'),
    path('checkout/', views.checkout, name='checkout'),
    path('confirm-order/', views.confirm_order, name='confirm_order'),
    path('thank-you/<int:order_id>/', views.thank_you , name='thank_you'),
    path('about/', views.about_view, name='about'),
    #path('menu/', views.menu_view, name='menu'),
    path('order-history/', views.order_history, name='order_history'),
    path('change-password/', views.change_password, name='change_password'),



    path('forgot-password/', views.forgot_password, name='forgot_password'),
    


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


