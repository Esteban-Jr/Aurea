from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),  # language switch (EN | ES)
    path('bookings/', include('bookings.urls')),
    path("accounts/", include("accounts.urls")),
    path('reviews/', include('reviews.urls')),
    path("", include("pages.urls")), 
]
