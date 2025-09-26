from django import forms
from .models import Booking
from django.core.exceptions import ValidationError
from django.forms import TextInput, DateInput, TimeInput, NumberInput, Textarea

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['name', 'date', 'time',
                  'guests', 'phone_number', 'email', 'special_requests']
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Your full name'}),
            'date': DateInput(attrs={'type': 'date'}),      
            'time': TimeInput(attrs={'type': 'time', 'step': 900}),  # 15-minute intervals  
            'guests': NumberInput(attrs={'min': 1, 'max': 25}),     
            'phone_number': TextInput(attrs={'placeholder': '7123456789'}),
            'special_requests': Textarea(attrs={'rows': 3}),
        }

# Server-side validation method
    def clean_booking_time(self):
        t = self.cleaned_data['booking_time']
        # Enforce 15-minute increments
        if t.minute % 15 != 0:
            raise ValidationError("Please choose a time in 15-minute intervals.")
        return t