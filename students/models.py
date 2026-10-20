
from django.db import models


class Student(models.Model):
    usn = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    department = models.CharField(max_length=100)
    academic_year = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.usn} - {self.name}"
