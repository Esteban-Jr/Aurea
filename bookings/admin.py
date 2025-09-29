from django.contrib import admin
from .models import Booking

# Customize how bookings appear in the admin list
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display  = ('name', 'phone_number', 'date', 'time', 'guests')
    list_filter   = ('date', 'time', 'guests')
    search_fields = ('name', 'phone_number')
    ordering      = ('-date', '-time')