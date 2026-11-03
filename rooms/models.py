
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q


class Hostel(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
    )
    block = models.CharField(
        max_length=50,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Hostel"
        verbose_name_plural = "Hostels"

    def __str__(self):
        return f"{self.name} - {self.block}"


class Room(models.Model):
    hostel = models.ForeignKey(
        Hostel,
        on_delete=models.CASCADE,
        related_name="rooms",
    )
    room_number = models.CharField(
        max_length=20,
    )
    capacity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
    )
    occupied_count = models.PositiveIntegerField(
        default=0,
    )

    @property
    def available_beds(self):
        return self.capacity - self.occupied_count

    class Meta:
        ordering = ["hostel__name", "room_number"]
        constraints = [
            models.UniqueConstraint(
                fields=["hostel", "room_number"],
                name="unique_room_number_per_hostel",
            ),
            models.CheckConstraint(
                condition=Q(capacity__gte=1),
                name="room_capacity_at_least_one",
            ),
            models.CheckConstraint(
                condition=(
                    Q(occupied_count__gte=0)
                    & Q(occupied_count__lte=models.F("capacity"))
                ),
                name="room_occupancy_within_capacity",
            ),
        ]

    def __str__(self):
        return f"{self.hostel.name} - Room {self.room_number}"
