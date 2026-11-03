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
    """Base exception for allocation-related service errors."""


class StudentNotFoundError(AllocationError):
    """Raised when the requested student does not exist."""


class StudentAlreadyAllocatedError(AllocationError):
    """Raised when the student already has an active allocation."""


class ActiveAllocationNotFoundError(AllocationError):
    """Raised when the student has no active room allocation."""


class SameRoomError(AllocationError):
    """Raised when the selected room is already assigned to the student."""


class AllocationService:
    """
    Provides transactional operations for student room allocations.

    All public service methods execute inside database transactions.
    Student, room, and allocation records are locked where required
    using select_for_update() to protect against concurrent changes.

    If an operation raises an exception, its transaction is rolled
    back, preventing partial updates to allocations and room occupancy.
    """

    @staticmethod
    @transaction.atomic
    def allocate_room(student_id, room_id):
        """
        Allocate a room to a student.

        Args:
            student_id (int): Primary key of the student.
            room_id (int): Primary key of the room to allocate.

        Returns:
            Allocation: The newly created active allocation.

        Raises:
            StudentNotFoundError: If the student does not exist or
                the supplied student ID is invalid.
            StudentAlreadyAllocatedError: If the student already
                has an active room allocation.
            RoomNotFoundError: If the requested room does not exist
                or the supplied room ID is invalid.
            RoomFullError: If the room has no available beds.
            RoomServiceError: If a room occupancy service operation
                fails.

        Transaction behaviour:
            The method runs inside transaction.atomic().
            It locks the student and requested room using
            select_for_update(), checks for an existing active
            allocation, reserves a bed, and creates the allocation.

            If any operation fails, the transaction rolls back.
            This ensures that a bed reservation cannot remain
            without its corresponding allocation record.
        """
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
        """
        Change a student's active room allocation.

        Args:
            student_id (int): Primary key of the student.
            new_room_id (int): Primary key of the destination room.

        Returns:
            Allocation: The newly created active allocation
                for the destination room.

        Raises:
            StudentNotFoundError: If the student does not exist or
                the supplied student ID is invalid.
            ActiveAllocationNotFoundError: If the student has no
                active allocation to change.
            RoomNotFoundError: If the destination room does not
                exist or its supplied ID is invalid.
            SameRoomError: If the destination is already the
                student's allocated room.
            RoomFullError: If the destination room has no
                available beds.
            RoomNotOccupiedError: If the old room has no occupied
                bed to release.
            RoomServiceError: If a room occupancy service operation
                fails.

        Transaction behaviour:
            The method runs inside transaction.atomic().
            It locks the student, current allocation, and destination
            room using select_for_update().

            It reserves a bed in the destination room, marks the old
            allocation as VACATED, records the vacation timestamp,
            releases the old room's bed, and creates a new ACTIVE
            allocation.

            All these changes belong to one transaction. If any
            operation fails, the transaction rolls back, preserving
            the previous allocation and room occupancy state.
        """
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
        """
        Vacate a student's currently active room allocation.

        Args:
            student_id (int): Primary key of the student.

        Returns:
            Allocation: The updated allocation with VACATED status
                and its vacation timestamp.

        Raises:
            StudentNotFoundError: If the student does not exist or
                the supplied student ID is invalid.
            ActiveAllocationNotFoundError: If the student has no
                active allocation to vacate.
            RoomNotFoundError: If the allocated room does not exist.
            RoomNotOccupiedError: If the allocated room has no
                occupied bed to release.
            RoomServiceError: If a room occupancy service operation
                fails.

        Transaction behaviour:
            The method runs inside transaction.atomic().
            It locks the student and active allocation using
            select_for_update(), marks the allocation as VACATED,
            records the vacation timestamp, and releases the room's
            occupied bed.

            If releasing the bed or another database operation fails,
            the transaction rolls back. The allocation therefore
            cannot be marked VACATED while its occupancy update fails.
            The allocation record is retained as history.
        """
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