"""Staff: see every booking, search and filter them, edit or cancel any of them."""
from datetime import date

from django.contrib import messages
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _

from aurea_project.staff import redirect_back, staff_required

from .forms import BookingForm
from .models import Booking

SHOW = ("today", "upcoming", "past", "all")


@staff_required
def booking_list(request):
    today = date.today()
    show = request.GET.get("show") if request.GET.get("show") in SHOW else "upcoming"
    on = request.GET.get("date", "")
    q = request.GET.get("q", "").strip()

    bookings = Booking.objects.select_related("user")
    if on:
        bookings = bookings.filter(date=on)
    elif show == "today":
        bookings = bookings.filter(date=today)
    elif show == "upcoming":
        bookings = bookings.filter(date__gte=today)
    elif show == "past":
        bookings = bookings.filter(date__lt=today)
    if q:
        bookings = bookings.filter(Q(name__icontains=q) | Q(email__icontains=q) |
                                   Q(phone_number__icontains=q) | Q(user__username__icontains=q))
    bookings = bookings.order_by("-date", "-time") if show == "past" else bookings.order_by("date", "time")

    todays = Booking.objects.filter(date=today)
    return render(request, "staff/booking_list.html", {
        "bookings": bookings,
        "show": show,
        "on": on,
        "q": q,
        "today_count": todays.count(),
        "today_guests": todays.aggregate(n=Sum("guests"))["n"] or 0,
        "filters": [("today", _("Today")), ("upcoming", _("Upcoming")), ("past", _("Past")), ("all", _("All"))],
    })


@staff_required
def booking_edit(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    form = BookingForm(request.POST or None, instance=booking, user=booking.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, _("The booking for %(name)s was updated.") % {"name": booking.name})
        return redirect_back(request, "staff_bookings")
    return render(request, "staff/booking_edit.html", {"form": form, "booking": booking,
                                                       "next": request.GET.get("next", "")})


@staff_required
def booking_cancel(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == "POST":
        booking.delete()
        messages.warning(request, _("The booking for %(name)s was cancelled.") % {"name": booking.name})
        return redirect("staff_bookings")
    return render(request, "staff/confirm_delete.html", {
        "title": _("Cancel booking"),
        "question": _("Cancel the booking for %(name)s on %(date)s at %(time)s?") % {
            "name": booking.name, "date": booking.date.strftime("%d/%m/%Y"), "time": booking.time.strftime("%H:%M")},
        "cancel_url": "staff_bookings",
    })
