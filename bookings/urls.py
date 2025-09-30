from django.urls import path
from . import views

urlpatterns = [
    path('book/', views.create_bookings, name='create_bookings'),
    path('booking-success/', views.booking_success, name='booking_success'),
    #edit booking
    #delete booking
]
