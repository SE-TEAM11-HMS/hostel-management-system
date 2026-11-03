
from django.db import transaction

from students.models import Student
from rooms.models import Room
from rooms.services import (
    RoomService,
    RoomFullError,
    RoomNotFoundError,
)

from .models import Allocation


class AllocationError(Exception):
    """Base exception for allocation errors."""


class StudentNotFoundError(AllocationError):
    """Raised when the student does not exist."""


class StudentAlreadyAllocatedError(AllocationError):
    """Raised when the student already has an active allocation."""


class AllocationService:

    @staticmethod
    @transaction.atomic
    def allocate_room(student_id, room_id):
        # Validate and retrieve the student safely.
        try:
            student = Student.objects.select_for_update().get(
                pk=student_id
            )
        except (Student.DoesNotExist, ValueError, TypeError):
            raise StudentNotFoundError(
                "The selected student does not exist."
            )

        # Prevent duplicate active allocations.
        if Allocation.objects.filter(
            student=student,
            status=Allocation.Status.ACTIVE,
        ).exists():
            raise StudentAlreadyAllocatedError(
                "This student already has an active room allocation."
            )

        # Lock and validate the room.
        try:
            Room.objects.select_for_update().get(pk=room_id)
        except (Room.DoesNotExist, ValueError, TypeError):
            raise RoomNotFoundError(
                "The selected room does not exist."
            )

        # Reserve a bed through the existing RoomService.
        RoomService.reserve_bed(room_id)

        # Create the active allocation.
        allocation = Allocation.objects.create(
            student=student,
            room_id=room_id,
            status=Allocation.Status.ACTIVE,
        )

        return allocation
