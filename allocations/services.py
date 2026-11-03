
from django.db import transaction
from django.utils import timezone

from students.models import Student
from rooms.models import Room
from rooms.services import (
    RoomService,
    RoomFullError,
    RoomNotFoundError,
    RoomNotOccupiedError,
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
        try:
            student = Student.objects.select_for_update().get(
                pk=student_id
            )
        except (Student.DoesNotExist, ValueError, TypeError):
            raise StudentNotFoundError(
                "The selected student does not exist."
            )

        if Allocation.objects.filter(
            student=student,
            status=Allocation.Status.ACTIVE,
        ).exists():
            raise StudentAlreadyAllocatedError(
                "This student already has an active room allocation."
            )

        try:
            Room.objects.select_for_update().get(pk=room_id)
        except (Room.DoesNotExist, ValueError, TypeError):
            raise RoomNotFoundError(
                "The selected room does not exist."
            )

        RoomService.reserve_bed(room_id)

        return Allocation.objects.create(
            student=student,
            room_id=room_id,
            status=Allocation.Status.ACTIVE,
        )

    @staticmethod
    @transaction.atomic
    def change_room(student_id, new_room_id):
        try:
            student = Student.objects.select_for_update().get(
                pk=student_id
            )
        except (Student.DoesNotExist, ValueError, TypeError):
            raise StudentNotFoundError(
                "The selected student does not exist."
            )

        try:
            old_allocation = Allocation.objects.select_for_update().get(
                student=student,
                status=Allocation.Status.ACTIVE,
            )
        except Allocation.DoesNotExist:
            raise ActiveAllocationNotFoundError(
                "This student has no active room allocation."
            )

        try:
            new_room = Room.objects.select_for_update().get(
                pk=new_room_id
            )
        except (Room.DoesNotExist, ValueError, TypeError):
            raise RoomNotFoundError(
                "The selected room does not exist."
            )

        if old_allocation.room_id == new_room.id:
            raise SameRoomError(
                "The student is already allocated to this room."
            )

        RoomService.reserve_bed(new_room.id)

        old_allocation.status = Allocation.Status.VACATED
        old_allocation.vacated_at = timezone.now()
        old_allocation.save(
            update_fields=["status", "vacated_at"]
        )

        RoomService.release_bed(old_allocation.room_id)

        return Allocation.objects.create(
            student=student,
            room=new_room,
            status=Allocation.Status.ACTIVE,
        )

    @staticmethod
    @transaction.atomic
    def vacate_room(student_id):
        """Vacate a student's active room allocation atomically."""

        try:
            student = Student.objects.select_for_update().get(
                pk=student_id
            )
        except (Student.DoesNotExist, ValueError, TypeError):
            raise StudentNotFoundError(
                "The selected student does not exist."
            )

        try:
            allocation = Allocation.objects.select_for_update().get(
                student=student,
                status=Allocation.Status.ACTIVE,
            )
        except Allocation.DoesNotExist:
            raise ActiveAllocationNotFoundError(
                "This student has no active room allocation."
            )

        allocation.status = Allocation.Status.VACATED
        allocation.vacated_at = timezone.now()
        allocation.save(
            update_fields=["status", "vacated_at"]
        )

        RoomService.release_bed(allocation.room_id)

        return allocation
