from django.db import migrations


def add_uk_prefix(apps, schema_editor):
    """Bookings used to store UK numbers without +44; store them in full now."""
    Booking = apps.get_model("bookings", "Booking")
    for booking in Booking.objects.exclude(phone_number__startswith="+"):
        booking.phone_number = "+44" + booking.phone_number.lstrip("0")
        booking.save(update_fields=["phone_number"])


def remove_uk_prefix(apps, schema_editor):
    Booking = apps.get_model("bookings", "Booking")
    for booking in Booking.objects.filter(phone_number__startswith="+44"):
        booking.phone_number = booking.phone_number[3:]
        booking.save(update_fields=["phone_number"])


class Migration(migrations.Migration):

    dependencies = [
        ("bookings", "0002_alter_booking_phone_number"),
    ]

    operations = [
        migrations.RunPython(add_uk_prefix, remove_uk_prefix),
    ]
