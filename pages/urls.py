from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"), 
    path("about/", views.about, name="about"),
    path("menu/", views.menu, name="menu"),
    path("faq/", views.faq, name="faq"),
    path("gallery/", views.gallery, name="gallery"),
]
