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
    path('acess_controller/', views.EventViews.as_view(), name='acess_controller'),
    path('acess_controller/search/', views.search_event_controller, name='search_event_controller'),
    path('acess_controller/controll_event<int:pk>/', views.EventControllView.as_view(), name='controll_event'),
    path('acess_controller/controll_event<int:pk>/ticket_detail', views.ticket_detail, name='ticket_detail'),
    path('acess_controller/controll_event<int:event_id>/validate/<str:ticket_hash>', views.validate_ticket, name='validate_ticket'),
    path('scan/', views.scan_qr, name='scan_qr'),


    path('organizer/events', views.organizer_events, name='organizer_events'),
    path('customer/event/about/<int:pk>/', views.EventAboutView.as_view(), name='aboutEvent'),
    path('customer/event/attractions/<int:pk>/', views.EventAttractionsView.as_view(), name='attractionsEvent'),
    path('customer/ticketsList/', views.TicketsListViews, name='ticketsList'),
    path('qr-code/<str:text>/', views.generate_qr_code, name='generate_qr_code'),
    
]