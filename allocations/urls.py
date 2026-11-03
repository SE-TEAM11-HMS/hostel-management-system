
from django.urls import path

from . import views

app_name = "allocations"

urlpatterns = [
    path(
        "allocate/",
        views.allocate_room,
        name="allocate_room",
    ),
    path(
        "change-room/<int:student_id>/",
        views.change_room,
        name="change_room",
    ),
    path(
        "vacate-room/<int:student_id>/",
        views.vacate_room,
        name="vacate_room",
    ),
]
