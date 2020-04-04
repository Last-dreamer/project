from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.loginPage, name='login'),
    path('logout', views.logoutUser, name='logout'),

    path('', views.home, name='home'),
    path('user', views.userPage, name='user'),

    path('products', views.products, name='products'),
    path('customer/<str:pk>', views.customer, name='customer'),
    path('createOrder/<str:pk>', views.createOrder, name='createOrder'),
    path('updateOrder/<str:pk>', views.updateOrder, name='updateOrder'),
    path('deleteOrder/<str:pk>', views.deleteOrder, name='deleteOrder'),
    path('setting', views.setting, name='setting'),

]
