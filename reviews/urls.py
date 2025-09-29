from django.urls import path
from . import views

urlpatterns = [
    path('', views.review_list, name='review_list'),
    path('add/', views.add_review, name='add_review'),
    path('<int:pk>/edit/', views.edit_review, name='edit_review'),
    path('<int:pk>/delete/', views.delete_review, name='delete_review'),
]
