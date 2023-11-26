from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'qualafesta'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/organizer', views.register_organizer, name='register_organizer'),
    path('register/customer',  views.register_customer, name='register_customer'),
    path('register/acess_controller',  views.register_acess_controller, name='register_acess_controller'),
    path('customer/', views.customer_index, name='customer'),
    path('organizer/', views.organizer_index, name='organizer'),
    path('organizer/events', views.organizer_events, name='organizer_events'),
    path('acess_controller/', views.acess_controller_index, name='acess_controller'),
    path('customer/event/about/<int:pk>/', views.EventAboutView.as_view(), name='aboutEvent'),
    path('customer/event/attractions/<int:pk>/', views.EventAttractionsView.as_view(), name='attractionsEvent'),
    path('customer/event/tickets/<int:pk>/', views.EventTicketsView.as_view(), name='ticketsEvent'),
    path('customer/ticketsList/', views.TicketsListViews, name='ticketsList'),
    path('customer/create_order/', views.create_order, name='createOrder'),
    path('qr-code/<str:text>/', views.generate_qr_code, name='generate_qr_code'),
    
]