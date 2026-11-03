
"""
URL configuration for hostel_project project.
"""

from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    # Accounts
    path("", include("accounts.urls")),

    # Django Admin
    path("admin/", admin.site.urls),

    # Student management
    path("students/", include("students.urls")),

    # Room management
    path("", include("rooms.urls")),

    # HOSTEL-28: Room allocation
    path("allocations/", include("allocations.urls")),
]
