from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .models import Booking
from .forms import BookingForm

# Only logged-in users can create bookings
@login_required
def create_bookings(request):
    # Display booking form pre-filled with user's info
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)  # Don't save yet
            booking.user = request.user        # Link booking to logged-in user
            booking.save()                     # Now save
            return redirect('booking_success')
    else:
        # Pre-fill the form with user's info
        initial_data = {
            'name': request.user.get_full_name(),  # full name from user model
            'email': request.user.email,  # pre-fill email from user model
            'phone_number': request.user.profile.phone_number if hasattr(request.user, 'profile') else ''
        }
        form = BookingForm(initial=initial_data)

    return render(request, 'bookings/create_bookings.html', {'form': form})

def booking_success(request):
    # Simple confirmation page shown after a successful booking.
    return render(request, 'bookings/booking_success.html')