from django.urls import path
from .views import EventList, EventDetail

urlpatterns = [
    path('events/<int:pk>/', EventDetail.as_view()),
    path('events/', EventList.as_view()),
    
]