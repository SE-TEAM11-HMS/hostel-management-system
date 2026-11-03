
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


class AllocationService:

    @staticmethod
    @transaction.atomic
    def allocate_room(student_id, room_id):

        # Lock the student row.
        try:
            student = Student.objects.select_for_update().get(
                pk=student_id
            )
        except Student.DoesNotExist:
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

        # Lock the room row to serialize allocations to this room.
        try:
            Room.objects.select_for_update().get(pk=room_id)
        except Room.DoesNotExist:
            raise RoomNotFoundError(
                "The selected room does not exist."
            )

        # Reserve a bed using the existing RoomService.
        RoomService.reserve_bed(room_id)

        # Create the allocation record.
        allocation = Allocation.objects.create(
            student=student,
            room_id=room_id,
            status=Allocation.Status.ACTIVE,
        )

        return allocation

    @staticmethod
    @transaction.atomic
    def vacate_room(allocation_id):

        try:
            allocation = Allocation.objects.select_for_update().get(
                pk=allocation_id,
                status=Allocation.Status.ACTIVE,
            )
        except Allocation.DoesNotExist:
            raise AllocationError(
                "Active allocation not found."
            )

        # Lock the room before releasing its bed.
        Room.objects.select_for_update().get(
            pk=allocation.room_id
        )

        RoomService.release_bed(allocation.room_id)

        allocation.status = Allocation.Status.VACATED
        allocation.vacated_at = timezone.now()
        allocation.save(
            update_fields=["status", "vacated_at"]
        )

        return allocation
