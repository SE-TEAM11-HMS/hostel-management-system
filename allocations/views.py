
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
    ActiveAllocationNotFoundError,
    SameRoomError,
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


@login_required
@require_http_methods(["GET", "POST"])
def change_room(request, student_id):
    # Only administrators can change room allocations.
    if not request.user.is_staff:
        return HttpResponseForbidden(
            "Only administrators can change room allocations."
        )

    try:
        student = Student.objects.get(pk=student_id)
    except (Student.DoesNotExist, ValueError, TypeError):
        messages.error(request, "Student does not exist.")
        return redirect("allocations:allocate_room")

    active_allocation = Allocation.objects.filter(
        student=student,
        status=Allocation.Status.ACTIVE,
    ).select_related("room").first()

    if active_allocation is None:
        messages.error(
            request,
            "This student has no active room allocation.",
        )
        return redirect("allocations:allocate_room")

    if request.method == "POST":
        new_room_id = request.POST.get("room_id")

        if not new_room_id:
            messages.error(
                request,
                "Please select a new room.",
            )
        else:
            try:
                AllocationService.change_room(
                    student_id=student_id,
                    new_room_id=new_room_id,
                )
                messages.success(
                    request,
                    "Room changed successfully.",
                )
                return redirect(
                    "allocations:change_room",
                    student_id=student_id,
                )

            except (
                StudentNotFoundError,
                ActiveAllocationNotFoundError,
                SameRoomError,
                RoomFullError,
                RoomNotFoundError,
                AllocationError,
            ) as error:
                messages.error(request, str(error))

    # Display rooms with available beds, excluding the current room.
    available_rooms = Room.objects.filter(
        occupied_count__lt=F("capacity")
    ).exclude(
        pk=active_allocation.room_id
    ).select_related("hostel").order_by(
        "hostel__name", "room_number"
    )

    return render(
        request,
        "allocations/change_room.html",
        {
            "student": student,
            "allocation": active_allocation,
            "rooms": available_rooms,
        },
    )
