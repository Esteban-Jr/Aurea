from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bookings/', include('bookings.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path("accounts/", include("accounts.urls")),
    path('reviews/', include('reviews.urls')),
]
