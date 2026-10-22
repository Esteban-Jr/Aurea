from django.db.models import Prefetch
from django.shortcuts import render

from .content import FAQ, GALLERY
from .models import Category, Dish


def home(request):
    signature = Dish.objects.filter(available=True, featured=True)[:3]
    return render(request, "pages/home.html", {"signature": signature})

def about(request):
    return render(request, "pages/about.html")

def menu(request):
    categories = Category.objects.prefetch_related(
        Prefetch("dishes", queryset=Dish.objects.filter(available=True), to_attr="visible_dishes")
    )
    menu = [c for c in categories if c.visible_dishes]
    # The pop-up card reads its text from this JSON (in the visitor's language)
    dish_data = {
        d.slug: {
            "name": d.name,
            "description": d.description,
            "story": d.story,
            "image": d.photo,
            "tags": d.tags,
            "allergens": d.allergen_labels,
        }
        for c in menu for d in c.visible_dishes
    }
    return render(request, "pages/menu.html", {"menu": menu, "dish_data": dish_data})

def faq(request):
    return render(request, "pages/faq.html", {"faq": FAQ})

def gallery(request):
    return render(request, "pages/gallery.html", {"photos": GALLERY})
