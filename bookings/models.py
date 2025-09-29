from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User


# Validator to make sure the user enters only UK local digits (no +44)
uk_number_validator = RegexValidator(
    regex=r'^\d{9,10}$',               # Accept 9–10 digits
    message="Enter the number without the +44 prefix."
)

# Create your models here.
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    guests = models.PositiveIntegerField()
    special_requests = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(
        max_length=10,                                  # up to 10 digits
        validators=[uk_number_validator],               # enforce digits only
        help_text="Enter the number without the +44 prefix."
    )


def full_phone(self):
        """
        Returns the full phone number with the +44 prefix,
        so templates or emails can display it correctly.
        """
        return f"+44{self.phone_number}"

def __str__(self):
        # Useful string representation for admin list
        return f"{self.name} - {self.date} at {self.time}"