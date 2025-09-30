from django.shortcuts import render

def home(request):
    return render(request, "pages/home.html")

def about(request):
    return render(request, "pages/about.html")

def menu(request):
    return render(request, "pages/menu.html")

def faq(request):
    return render(request, "pages/faq.html")

def gallery(request):
    return render(request, "pages/gallery.html")
