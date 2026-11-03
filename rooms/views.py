
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from .forms import HostelForm, RoomForm
from .models import Hostel, Room


def administrator_required(request):
    return request.user.is_staff


@login_required
@require_http_methods(["GET"])
def room_list(request):
    if not administrator_required(request):
        return HttpResponseForbidden(
            "You do not have permission to manage hostel rooms."
        )

    hostels = Hostel.objects.prefetch_related("rooms").all()
    rooms = Room.objects.select_related("hostel").all()

    return render(
        request,
        "rooms/room_list.html",
        {
            "hostels": hostels,
            "rooms": rooms,
        },
    )


@login_required
@require_http_methods(["GET", "POST"])
def add_hostel(request):
    if not administrator_required(request):
        return HttpResponseForbidden(
            "You do not have permission to add hostels."
        )

    form = HostelForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        try:
            with transaction.atomic():
                form.save()
        except IntegrityError:
            form.add_error(
                "name",
                "A hostel with this name already exists."
            )
        else:
            messages.success(request, "Hostel added successfully.")
            return redirect("rooms:room_list")

    return render(
        request,
        "rooms/add_hostel.html",
        {"form": form},
    )


@login_required
@require_http_methods(["GET", "POST"])
def add_room(request):
    if not administrator_required(request):
        return HttpResponseForbidden(
            "You do not have permission to add rooms."
        )

    form = RoomForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        try:
            with transaction.atomic():
                form.save()
        except IntegrityError:
            form.add_error(
                "room_number",
                "This room already exists in the selected hostel."
            )
        else:
            messages.success(request, "Room added successfully.")
            return redirect("rooms:room_list")

    return render(
        request,
        "rooms/add_room.html",
        {"form": form},
    )
