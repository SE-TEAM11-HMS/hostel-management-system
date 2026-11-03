
from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    # Administrator authentication
    path("login/", views.admin_login, name="login"),
    path("logout/", views.admin_logout, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),

    # Student authentication and portal
    path("student-login/", views.student_login, name="student_login"),
    path("student-portal/", views.student_portal, name="student_portal"),
    path("student-logout/", views.student_logout, name="student_logout"),
]
