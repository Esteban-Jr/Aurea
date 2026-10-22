from django import forms
from django.core.exceptions import ValidationError
from django.forms import TextInput, DateInput, NumberInput, Textarea
from datetime import datetime, date
from django.utils.translation import gettext as _, gettext_lazy
from accounts import phone
from .models import Booking

# Every 30 minutes between 09:00–21:00
TIME_CHOICES = [(f"{h:02d}:{m:02d}", f"{h:02d}:{m:02d}") for h in range(9, 22) for m in (0, 30)]

class BookingForm(forms.ModelForm):
    time = forms.ChoiceField(
        choices=TIME_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    # Any country: the picker defaults to the UK, the number is stored as +447123456789
    phone_country = phone.country_field(required=False)
    phone_number = phone.number_field()

    class Meta:
        model = Booking
        fields = ['name', 'date', 'time', 'guests', 'phone_number', 'email', 'special_requests']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': gettext_lazy('Your full name')}),
            'date': DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),  # date inputs need ISO, whatever the language
            'guests': NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 25}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': gettext_lazy('Your email')}),
            'special_requests': Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': gettext_lazy('Any special requests?')
            }),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # Show a saved number as country + local part again
        saved = self.initial.get('phone_number', '')
        if saved.startswith('+') and not self.is_bound:
            self.initial['phone_country'], self.initial['phone_number'] = phone.split(saved)

    def clean_phone_number(self):
        return phone.to_e164(self.data.get('phone_country') or phone.DEFAULT_COUNTRY,
                             self.cleaned_data['phone_number'])

    def clean(self):
        cleaned = super().clean()
        d = cleaned.get("date")
        t_str = cleaned.get("time")

        if d:
            today = date.today()
            now = datetime.now().time()

            # Editing: prevent editing past bookings
            if self.instance and self.instance.pk and self.instance.date < today:
                raise ValidationError(_("Past bookings cannot be edited."))

            # Prevent selecting past dates
            if d < today:
                raise ValidationError(_("You cannot book a date in the past."))

            # Prevent past times for today
            if d == today and t_str:
                t = datetime.strptime(t_str, "%H:%M").time()
                if t <= now:
                    raise ValidationError(_("You cannot book a time that has already passed today."))

        # Prevent double booking
        if self.user and d and t_str:
            t = datetime.strptime(t_str, "%H:%M").time()  # convert string to time
            exists = Booking.objects.filter(
                user=self.user, date=d, time=t
            ).exclude(id=self.instance.id if self.instance else None).exists()
            if exists:
                raise ValidationError(_("You already have a booking at this time."))

        return cleaned