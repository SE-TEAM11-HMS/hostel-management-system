from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from .services import (
    AllocationService,
    AllocationError,
    StudentNotFoundError,
    StudentAlreadyAllocatedError,
)

from rooms.services import RoomFullError, RoomNotFoundError


@login_required
@require_POST
def allocate_room(request):

    # Only administrators can allocate rooms.
    if not request.user.is_staff:
        return HttpResponseForbidden(
            "Only administrators can allocate rooms."
        )

    student_id = request.POST.get("student_id")
    room_id = request.POST.get("room_id")

    if not student_id or not room_id:
        messages.error(
            request,
            "Please select both a student and a room.",
        )
        return redirect("accounts:dashboard")

    try:
        AllocationService.allocate_room(
            student_id=student_id,
            room_id=room_id,
        )

        messages.success(
            request,
            "Room allocated successfully.",
        )

    except StudentNotFoundError as error:
        messages.error(request, str(error))

    except StudentAlreadyAllocatedError as error:
        messages.error(request, str(error))

    except (RoomFullError, RoomNotFoundError) as error:
        messages.error(request, str(error))

    except AllocationError as error:
        messages.error(request, str(error))

    return redirect("accounts:dashboard")