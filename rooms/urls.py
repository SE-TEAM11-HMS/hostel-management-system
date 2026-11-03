from django.urls import path
from . import views

app_name = "rooms"

urlpatterns = [
    # Hostel and room management (HOSTEL-24)
    path("rooms/", views.room_list, name="room_list"),
    path("hostels/add/", views.add_hostel, name="hostel_add"),
    path("rooms/add/", views.add_room, name="room_add"),

    # Room availability and details (HOSTEL-25)
    path(
        "rooms/available/",
        views.available_rooms,
        name="available_rooms",
    ),
    path(
        "rooms/occupied/",
        views.occupied_rooms,
        name="occupied_rooms",
    ),
    path(
        "rooms/<int:room_id>/",
        views.room_detail,
        name="room_detail",
    ),
]
