from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

admin.site.site_header = "Aurea admin"
admin.site.site_title = "Aurea admin"
admin.site.index_title = "Restaurant"
admin.site.site_url = "/"        # the "View site" link goes back to the website

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),  # language switch (EN | ES)
    path('bookings/', include('bookings.urls')),
    path("accounts/", include("accounts.urls")),
    path('reviews/', include('reviews.urls')),
    path("", include("pages.urls")), 
]

if settings.DEBUG:  # local preview: serve uploaded dish photos
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
