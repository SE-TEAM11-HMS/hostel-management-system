
from django.db import transaction
from django.db.models import F

from .models import Room


class RoomServiceError(Exception):
    """Base exception for room occupancy service errors."""


class RoomNotFoundError(RoomServiceError):
    """Raised when the requested room does not exist."""


class RoomFullError(RoomServiceError):
    """Raised when a room has no available beds."""


class RoomNotOccupiedError(RoomServiceError):
    """Raised when trying to release a bed from an empty room."""


class RoomService:
    """Provides atomic room occupancy operations."""

    @staticmethod
    @transaction.atomic
    def reserve_bed(room_id):
        """Reserve one bed if the room has available capacity."""

        updated = Room.objects.filter(
            pk=room_id,
            occupied_count__lt=F("capacity"),
        ).update(
            occupied_count=F("occupied_count") + 1
        )

        if updated == 0:
            if not Room.objects.filter(pk=room_id).exists():
                raise RoomNotFoundError(
                    f"Room with ID {room_id} does not exist."
                )

            raise RoomFullError(
                f"Room with ID {room_id} is full."
            )

        return Room.objects.get(pk=room_id)

    @staticmethod
    @transaction.atomic
    def release_bed(room_id):
        """Release one occupied bed."""

        updated = Room.objects.filter(
            pk=room_id,
            occupied_count__gt=0,
        ).update(
            occupied_count=F("occupied_count") - 1
        )

        if updated == 0:
            if not Room.objects.filter(pk=room_id).exists():
                raise RoomNotFoundError(
                    f"Room with ID {room_id} does not exist."
                )

            raise RoomNotOccupiedError(
                f"Room with ID {room_id} has no occupied beds."
            )

        return Room.objects.get(pk=room_id)
