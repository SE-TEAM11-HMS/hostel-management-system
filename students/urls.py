
from django.urls import path
from . import views

urlpatterns = [
    path("add/", views.add_student, name="student_add"),
]
