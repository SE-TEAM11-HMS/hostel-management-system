
from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError


class Student(models.Model):
    usn = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100, db_index=True)
    email = models.EmailField(unique=True)

    phone = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r"^\d{10}$",
                message="Phone number must contain exactly 10 digits.",
            )
        ],
    )

    department = models.CharField(max_length=100)
    academic_year = models.PositiveSmallIntegerField()

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="student",
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(academic_year__gte=1, academic_year__lte=4),
                name="student_academic_year_1_to_4",
            ),
            models.CheckConstraint(
                condition=Q(phone__regex=r"^[0-9]{10}$"),
                name="student_phone_exactly_10_digits",
            ),
        ]

    def clean(self):
        super().clean()

        if (
            not self.phone.isascii()
            or not self.phone.isdigit()
            or len(self.phone) != 10
        ):
            raise ValidationError({
                "phone": "Phone number must contain exactly 10 digits."
            })

    def __str__(self):
        return f"{self.usn} - {self.name}"
