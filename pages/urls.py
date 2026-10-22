from django.urls import path

from . import staff_views, views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("menu/", views.menu, name="menu"),
    path("faq/", views.faq, name="faq"),
    path("gallery/", views.gallery, name="gallery"),

    # Staff: Manage menu
    path("staff/menu/", staff_views.manage_menu, name="manage_menu"),
    path("staff/menu/dish/new/", staff_views.dish_form, name="dish_create"),
    path("staff/menu/dish/<int:pk>/edit/", staff_views.dish_form, name="dish_edit"),
    path("staff/menu/dish/<int:pk>/delete/", staff_views.dish_delete, name="dish_delete"),
    path("staff/menu/dish/<int:pk>/toggle/", staff_views.dish_toggle, name="dish_toggle"),
    path("staff/menu/category/new/", staff_views.category_form, name="category_create"),
    path("staff/menu/category/<int:pk>/edit/", staff_views.category_form, name="category_edit"),
    path("staff/menu/category/<int:pk>/delete/", staff_views.category_delete, name="category_delete"),
]
