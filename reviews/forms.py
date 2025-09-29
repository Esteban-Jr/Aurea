from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'rating']
        widgets = {
            # Radio buttons for 1–5
            'rating': forms.RadioSelect(
                choices=[(i, '★' * i) for i in range(1, 6)]
            ),
        }
