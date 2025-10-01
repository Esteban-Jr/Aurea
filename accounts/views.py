from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from .forms import SignUpForm, UserUpdateForm
from django.contrib.auth import logout
from bookings.models import Booking
from datetime import date

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

class LoginViewCustom(LoginView):
    template_name = 'registration/login.html'

@login_required
def logout_confirm(request):
    if request.method == "POST":
        logout(request)
        return redirect("home")  # after logging out, send them to home page
    return render(request, "registration/logout.html")

@login_required
def profile_view(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-date', '-time')
    return render(request, 'accounts/profile.html', {
        'bookings': bookings,
        'today': date.today()
    })

@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'accounts/profile_edit.html', {'form': form})

from django.shortcuts import render

def preview_template(request, name):
    """
    Quick way to preview password templates without migrations or email.
    Example:  /accounts/preview/password_reset.html
    """
    return render(request, f"accounts/{name}")