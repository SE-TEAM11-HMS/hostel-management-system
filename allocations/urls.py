from django.urls import path

from . import views

app_name = "allocations"

urlpatterns = [
    path(
        "allocate/",
        views.allocate_room,
        name="allocate_room",
    ),
]