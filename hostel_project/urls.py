
"""
URL configuration for hostel_project project.
"""

from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("", include("accounts.urls")),
    path("admin/", admin.site.urls),
    path("students/", include("students.urls")),
    path("", include("rooms.urls")),
]
