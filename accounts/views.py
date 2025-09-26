from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm

# Create your views here.
def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # automatically log in the new user
            return redirect("/")  # redirect to home page or dashboard
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {"form": form})