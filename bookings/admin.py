from django.contrib import admin
from .models import Booking

# Customize how bookings appear in the admin list
class BookingAdmin(admin.ModelAdmin):
    # Columns to show in the list view
    list_display = (
        'name',               # the name of the person booking
        'phone_number',       # their phone number
        'date',       # date of the booking
        'time',       # time of the booking
        'guests',             # number of guests
    )

    # Add filters in the right-hand sidebar
    list_filter = ('date', 'time', 'guests')

    # Add a search bar
    search_fields = ('name', 'phone_number')

    # Optional: order newest bookings first
    ordering = ('-date', '-time')

# Register the model with the custom admin options
admin.site.register(Booking, BookingAdmin)