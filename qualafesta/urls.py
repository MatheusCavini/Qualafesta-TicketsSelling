from django.urls import path

from . import views
from django.contrib.auth.views import LogoutView

app_name = 'qualafesta'
urlpatterns = [
    path('', views.index, name='index'),
    path('customer/', views.customer_index, name='customer'),
    path('login/', views.login, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/',views.register, name='register'),
    path('register/organizer', views.register_organizer, name='register_organizer'),
    path('register/customer',  views.register_customer, name='register_customer')
]