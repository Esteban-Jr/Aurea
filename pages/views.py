from django.shortcuts import render

from .content import FAQ, GALLERY, MENU, SIGNATURE


def all_dishes():
    return [d for category in MENU for d in category["dishes"]]


def home(request):
    dishes = {d["name"]: d for d in all_dishes()}
    return render(request, "pages/home.html", {"signature": [dishes[n] for n in SIGNATURE]})

def about(request):
    return render(request, "pages/about.html")

def menu(request):
    # The pop-up card reads its text from this JSON (strings already in the visitor's language)
    dish_data = {
        d["slug"]: {
            "name": d["name"],
            "description": str(d["description"]),
            "story": str(d["story"]),
            "image": d["image"],
            "tags": [str(t) for t in d["tags"]],
            "allergens": [str(a) for a in d["allergens"]],
        }
        for d in all_dishes()
    }
    return render(request, "pages/menu.html", {"menu": MENU, "dish_data": dish_data})

def faq(request):
    return render(request, "pages/faq.html", {"faq": FAQ})

def gallery(request):
    return render(request, "pages/gallery.html", {"photos": GALLERY})
