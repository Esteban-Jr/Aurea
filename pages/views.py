from django.shortcuts import render

from .content import FAQ, GALLERY, MENU, SIGNATURE


def home(request):
    dishes = {d[0]: d for cat in MENU for d in cat["dishes"]}
    return render(request, "pages/home.html", {"signature": [dishes[n] for n in SIGNATURE]})

def about(request):
    return render(request, "pages/about.html")

def menu(request):
    return render(request, "pages/menu.html", {"menu": MENU})

def faq(request):
    return render(request, "pages/faq.html", {"faq": FAQ})

def gallery(request):
    return render(request, "pages/gallery.html", {"photos": GALLERY})
