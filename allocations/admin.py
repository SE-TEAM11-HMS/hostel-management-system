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

    list_filter = ("status", "allocated_at")

    search_fields = (
        "student__usn",
        "student__name",
        "room__room_number",
        "room__hostel__name",
    )

    readonly_fields = (
        "student",
        "room",
        "status",
        "active_student",
        "allocated_at",
        "vacated_at",
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False