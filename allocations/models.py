from django.db import models
from django.db.models import Q

from students.models import Student
from rooms.models import Room


class Allocation(models.Model):

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        VACATED = "VACATED", "Vacated"

    student = models.ForeignKey(
        Student,
        on_delete=models.PROTECT,
        related_name="allocations",
    )

    room = models.ForeignKey(
        Room,
        on_delete=models.PROTECT,
        related_name="allocations",
    )

    # Stores the student only while this allocation is active.
    # MySQL allows multiple NULL values in a unique column.
    active_student = models.ForeignKey(
        Student,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        editable=False,
        related_name="+",
    )

    allocated_at = models.DateTimeField(auto_now_add=True)

    vacated_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    class Meta:
        ordering = ["-allocated_at"]

        constraints = [
            models.UniqueConstraint(
                fields=["active_student"],
                name="unique_active_allocation_per_student",
            ),
            models.CheckConstraint(
                condition=(
                    Q(status="ACTIVE", vacated_at__isnull=True)
                    | Q(status="VACATED", vacated_at__isnull=False)
                ),
                name="allocation_status_vacated_at_consistent",
            ),
        ]

    def save(self, *args, **kwargs):
        if self.status == self.Status.ACTIVE:
            self.active_student_id = self.student_id
        else:
            self.active_student_id = None

        update_fields = kwargs.get("update_fields")
        if update_fields is not None:
            kwargs["update_fields"] = set(update_fields) | {
                "active_student"
            }

        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.student.usn} - "
            f"{self.room} - {self.status}"
        )