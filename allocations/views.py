from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from students.models import Student
from rooms.models import Room
from rooms.services import RoomFullError, RoomNotFoundError

from .models import Allocation
from .services import (
    AllocationService,
    AllocationError,
    StudentNotFoundError,
    StudentAlreadyAllocatedError,
)


@login_required
@require_http_methods(["GET", "POST"])
def allocate_room(request):
    # Only administrators can access this page.
    if not request.user.is_staff:
        return HttpResponseForbidden(
            "Only administrators can allocate rooms."
        )

    if request.method == "POST":
        student_id = request.POST.get("student_id")
        room_id = request.POST.get("room_id")

        if not student_id or not room_id:
            messages.error(
                request,
                "Please select both a student and a room.",
            )
        else:
            try:
                AllocationService.allocate_room(
                    student_id=student_id,
                    room_id=room_id,
                )
                messages.success(
                    request,
                    "Room allocated successfully.",
                )
            except (
                StudentNotFoundError,
                StudentAlreadyAllocatedError,
                RoomFullError,
                RoomNotFoundError,
                AllocationError,
            ) as error:
                messages.error(request, str(error))

        return redirect("allocations:allocate_room")

    # Students who do not already have an active allocation.
    eligible_students = Student.objects.exclude(
        allocations__status=Allocation.Status.ACTIVE
    ).distinct().order_by("name")

    # Rooms that still have available beds.
    available_rooms = Room.objects.filter(
        occupied_count__lt=F("capacity")
    ).select_related("hostel").order_by(
        "hostel__name", "room_number"
    )

    return render(
        request,
        "allocations/allocate_room.html",
        {
            "students": eligible_students,
            "rooms": available_rooms,
        },
    )