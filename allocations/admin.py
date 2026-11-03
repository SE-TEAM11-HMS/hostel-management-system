
from django.contrib import admin

from .models import Allocation


@admin.register(Allocation)
class AllocationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "student",
        "room",
        "status",
        "allocated_at",
        "vacated_at",
    )

    list_filter = (
        "status",
        "allocated_at",
    )

    search_fields = (
        "student__usn",
        "student__name",
        "room__room_number",
        "room__hostel__name",
    )

    readonly_fields = (
        "allocated_at",
    )
