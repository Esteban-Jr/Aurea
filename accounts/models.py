from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    """Extra details for a user. Created on sign-up, or the first time it's needed."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    phone = models.CharField(_("phone"), max_length=20, blank=True,
                             help_text=_("International format, e.g. +573001234567"))

    def __str__(self):
        return f"{self.user.username} ({self.phone or 'no phone'})"
