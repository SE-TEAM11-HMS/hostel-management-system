
from django.urls import path
from . import views

app_name = "rooms"

urlpatterns = [
    path("rooms/", views.room_list, name="room_list"),
    path("hostels/add/", views.add_hostel, name="hostel_add"),
    path("rooms/add/", views.add_room, name="room_add"),
]
