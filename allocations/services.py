
from django.db import transaction
from django.utils import timezone

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


class ActiveAllocationNotFoundError(AllocationError):
    """Raised when the student has no active room allocation."""


class SameRoomError(AllocationError):
    """Raised when the selected room is already assigned."""


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

    @staticmethod
    @transaction.atomic
    def change_room(student_id, new_room_id):
        # Lock and validate the student.
        try:
            student = Student.objects.select_for_update().get(
                pk=student_id
            )
        except (Student.DoesNotExist, ValueError, TypeError):
            raise StudentNotFoundError(
                "The selected student does not exist."
            )

        # Find and lock the student's active allocation.
        try:
            old_allocation = Allocation.objects.select_for_update().get(
                student=student,
                status=Allocation.Status.ACTIVE,
            )
        except Allocation.DoesNotExist:
            raise ActiveAllocationNotFoundError(
                "This student has no active room allocation."
            )

        # Lock and validate the new room.
        try:
            new_room = Room.objects.select_for_update().get(
                pk=new_room_id
            )
        except (Room.DoesNotExist, ValueError, TypeError):
            raise RoomNotFoundError(
                "The selected room does not exist."
            )

        # Prevent selecting the current room.
        if old_allocation.room_id == new_room.id:
            raise SameRoomError(
                "The student is already allocated to this room."
            )

        # Reserve a bed in the new room.
        RoomService.reserve_bed(new_room.id)

        # Vacate the old allocation.
        old_allocation.status = Allocation.Status.VACATED
        old_allocation.vacated_at = timezone.now()
        old_allocation.save(
            update_fields=["status", "vacated_at"]
        )

        # Release the bed in the old room.
        RoomService.release_bed(old_allocation.room_id)

        # Create the new active allocation.
        new_allocation = Allocation.objects.create(
            student=student,
            room=new_room,
            status=Allocation.Status.ACTIVE,
        )

        return new_allocation
