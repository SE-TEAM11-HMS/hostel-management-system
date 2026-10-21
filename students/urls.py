from django.urls import path
from . import views

urlpatterns = [
    path("", views.student_list, name="student_list"),
    path("add/", views.add_student, name="student_add"),
    path("<int:pk>/", views.student_detail, name="student_detail"),
]