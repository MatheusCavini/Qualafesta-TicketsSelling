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
    path('customer/', views.CustomerIndex, name='customer'),

    path('organizer/', views.organizer_index, name='organizer'),
    path('acess_controller/', views.EventControllerViews.as_view(), name='acess_controller'),
    path('acess_controller/search/', views.search_event_controller, name='search_event_controller'),
    path('acess_controller/controll_event<int:pk>/', views.EventControllView.as_view(), name='controll_event'),
    path('acess_controller/controll_event<int:pk>/ticket_detail', views.ticket_detail, name='ticket_detail'),
    path('acess_controller/controll_event<int:event_id>/validate/<str:ticket_hash>', views.validate_ticket, name='validate_ticket'),
    path('acess_controller/profile/', views.acess_controller_profile, name='acessControllerProfile'),
    path('scan/', views.scan_qr, name='scan_qr'),
    path('organizer/events', views.EventListView.as_view(), name='organizer_events'),
    path('organizer/createEvent', views.create_event, name='create_event'),
    path('organizer/event/about/<int:pk>/', views.OrgEventAboutView.as_view(), name='detail_event'),
    path('organizer/event/about/<int:pk>/attractions/', views.OrgAttractionsView.as_view(), name='event_attractions'),
    path('organizer/event/about/<int:pk>/createAttraction/', views.create_attraction, name = 'create_attraction'),
    path('organizer/event/about/tickets/<int:pk>/', views.OrgTicketsView.as_view(), name='event_tickets'),
    path('organizer/event/about/<int:pk>/createTicket/', views.create_ticket, name = 'create_ticket'),
    path('organizer/event/updateEvent/<int:pk>/', views.UpdateEventView.as_view(), name='update_event'), 
    path('organizer/profile/', views.organizer_profile, name='organizerProfile'),

    
    path('customer/event/about/<int:pk>/', views.EventAboutView.as_view(), name='aboutEvent'),
    path('customer/event/attractions/<int:pk>/', views.EventAttractionsView.as_view(), name='attractionsEvent'),
    path('customer/event/tickets/<int:pk>/', views.EventTicketsView.as_view(), name='ticketsEvent'),
    path('customer/ticketsList/', views.TicketsListViews, name='ticketsList'),
    path('customer/create_order/', views.create_order, name='createOrder'),
    path('customer/create_purchased_tickets/', views.create_purchased_tickets, name='createTickets'),
    path('customer/profile/', views.CustomerProfile, name='customerProfile'),
    path('qr-code/<str:text>/', views.generate_qr_code, name='generate_qr_code'),
    path('search/', views.search_events, name='search'),
    
]