from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display  = ('user', 'rating', 'approved', 'created_at')
    list_filter   = ('approved', 'rating', 'created_at')
    search_fields = ('user__username', 'comment')
    ordering      = ('-created_at',)

    def star_rating(self, obj):
        return '★' * obj.rating + '☆' * (5 - obj.rating)
    star_rating.short_description = "Rating"