from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.db.models import F
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import HostelForm, RoomForm
from .models import Hostel, Room


def administrator_required(request):
    return request.user.is_staff


def filter_rooms_by_hostel(request, rooms):
    hostel_id = request.GET.get("hostel", "").strip()

    if hostel_id:
        if hostel_id.isdigit():
            rooms = rooms.filter(hostel_id=hostel_id)
        else:
            rooms = rooms.none()

    return rooms, hostel_id


# HOSTEL-24: Room management
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
@require_http_methods(["GET"])
def available_rooms(request):
    if not administrator_required(request):
        return HttpResponseForbidden(
            "You do not have permission to view room availability."
        )

    rooms = Room.objects.select_related("hostel").filter(
        occupied_count__lt=F("capacity")
    )

    rooms, selected_hostel = filter_rooms_by_hostel(request, rooms)
    hostels = Hostel.objects.all()

    return render(
        request,
        "rooms/available_rooms.html",
        {
            "rooms": rooms,
            "hostels": hostels,
            "selected_hostel": selected_hostel,
        },
    )


@login_required
@require_http_methods(["GET"])
def occupied_rooms(request):
    if not administrator_required(request):
        return HttpResponseForbidden(
            "You do not have permission to view occupied rooms."
        )

    rooms = Room.objects.select_related("hostel").filter(
        occupied_count__gt=0
    )

    rooms, selected_hostel = filter_rooms_by_hostel(request, rooms)
    hostels = Hostel.objects.all()

    return render(
        request,
        "rooms/occupied_rooms.html",
        {
            "rooms": rooms,
            "hostels": hostels,
            "selected_hostel": selected_hostel,
        },
    )


@login_required
@require_http_methods(["GET"])
def room_detail(request, room_id):
    if not administrator_required(request):
        return HttpResponseForbidden(
            "You do not have permission to view room details."
        )

    room = get_object_or_404(
        Room.objects.select_related("hostel"),
        pk=room_id,
    )

    return render(
        request,
        "rooms/room_detail.html",
        {"room": room},
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


# HOSTEL-25: Room availability and details

@login_required
@require_http_methods(["GET"])
def available_rooms(request):
    if not administrator_required(request):
        return HttpResponseForbidden(
            "You do not have permission to view room availability."
        )

    rooms = Room.objects.select_related("hostel").filter(
        occupied_count__lt=F("capacity")
    )

    rooms, selected_hostel = filter_rooms_by_hostel(request, rooms)

    return render(
        request,
        "rooms/available_rooms.html",
        {
            "rooms": rooms,
            "hostels": Hostel.objects.all(),
            "selected_hostel": selected_hostel,
        },
    )


@login_required
@require_http_methods(["GET"])
def occupied_rooms(request):
    if not administrator_required(request):
        return HttpResponseForbidden(
            "You do not have permission to view occupied rooms."
        )

    rooms = Room.objects.select_related("hostel").filter(
        occupied_count__gt=0
    )

    rooms, selected_hostel = filter_rooms_by_hostel(request, rooms)

    return render(
        request,
        "rooms/occupied_rooms.html",
        {
            "rooms": rooms,
            "hostels": Hostel.objects.all(),
            "selected_hostel": selected_hostel,
        },
    )


@login_required
@require_http_methods(["GET"])
def room_detail(request, room_id):
    if not administrator_required(request):
        return HttpResponseForbidden(
            "You do not have permission to view room details."
        )

    room = get_object_or_404(
        Room.objects.select_related("hostel"),
        pk=room_id,
    )

    return render(
        request,
        "rooms/room_detail.html",
        {"room": room},
    )