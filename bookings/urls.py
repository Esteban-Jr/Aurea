from django.urls import path
from . import views

urlpatterns = [
    path('book/', views.create_bookings, name='create_bookings'),
    path('booking-success/', views.booking_success, name='booking_success'),
    path('<int:pk>/edit/', views.edit_booking, name='edit_booking'),
    path('<int:pk>/delete/', views.delete_booking, name='delete_booking'),
]
