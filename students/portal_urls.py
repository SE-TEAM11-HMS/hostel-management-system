from django.urls import path
from . import views

urlpatterns = [
    path("portal/", views.student_portal, name="student_portal"),
    path("portal/room/", views.student_portal_room, name="student_portal_room"),
]