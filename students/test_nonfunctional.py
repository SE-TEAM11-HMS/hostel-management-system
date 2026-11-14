from time import perf_counter

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from allocations.models import Allocation
from allocations.services import AllocationService
from rooms.models import Hostel, Room
from students.models import Student


class NonFunctionalPerformanceTests(TestCase):
    response_time_target_seconds = 3.0

    def setUp(self):
        self.admin = get_user_model().objects.create_user(
            username="nfr_admin",
            password="NfrPass!234",
            is_staff=True,
        )
        self.client.force_login(self.admin)

        self.hostel = Hostel.objects.create(
            name="NFR Test Hostel",
            block="A",
        )
        self.room = Room.objects.create(
            hostel=self.hostel,
            room_number="101",
            capacity=3,
        )

    def timed_get(self, url, **params):
        started = perf_counter()
        response = self.client.get(url, params)
        duration = perf_counter() - started
        self.assertEqual(response.status_code, 200)
        self.assertLess(
            duration,
            self.response_time_target_seconds,
            f"{url} exceeded the three-second response-time target.",
        )
        return duration

    def test_primary_interfaces_render_with_clear_headings(self):
        pages = (
            (reverse("accounts:dashboard"), "Administrator dashboard"),
            (reverse("student_list"), "Student directory"),
            (reverse("rooms:room_list"), "Hostels and rooms"),
            (reverse("allocations:allocate_room"), "Allocate Room to Student"),
        )

        for url, heading in pages:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, heading)

    def test_normal_admin_operations_meet_response_time_target(self):
        Student.objects.create(
            usn="NFR001",
            name="Normal Operation Student",
            email="nfr001@example.com",
            phone="9876543210",
            department="CSE",
            academic_year=2,
        )

        measurements = {
            "dashboard": self.timed_get(reverse("accounts:dashboard")),
            "student_list": self.timed_get(reverse("student_list")),
            "available_rooms": self.timed_get(
                reverse("rooms:available_rooms")
            ),
            "allocation_form": self.timed_get(
                reverse("allocations:allocate_room")
            ),
        }
        for name, duration in measurements.items():
            print(
                "NFR_METRIC "
                f"operation={name} duration_seconds={duration:.6f}"
            )

    def test_short_run_availability_probe_has_no_failed_requests(self):
        durations = []
        for _ in range(20):
            durations.append(self.timed_get(reverse("student_list")))

        print(
            "NFR_METRIC "
            "availability_probe_requests=20 "
            f"max_duration_seconds={max(durations):.6f}"
        )

    def test_student_list_scales_through_500_records(self):
        targets = (25, 250, 500)
        created = 0

        for target in targets:
            students = []
            for index in range(created, target):
                students.append(
                    Student(
                        usn=f"SCALE{index:04d}",
                        name=f"Scale Student {index}",
                        email=f"scale{index}@example.com",
                        phone=f"9{index:09d}",
                        department="CSE",
                        academic_year=2,
                    )
                )
            Student.objects.bulk_create(students)
            created = target

            duration = self.timed_get(
                reverse("student_list"),
                q="SCALE",
            )
            self.assertEqual(
                Student.objects.filter(usn__startswith="SCALE").count(),
                target,
            )
            print(
                "NFR_METRIC "
                f"student_records={target} "
                f"list_duration_seconds={duration:.6f}"
            )

    def test_integrated_allocation_and_vacation_remain_consistent(self):
        student = Student.objects.create(
            usn="NFR002",
            name="Consistency Student",
            email="nfr002@example.com",
            phone="9876543211",
            department="ISE",
            academic_year=3,
        )

        allocation = AllocationService.allocate_room(
            student.pk,
            self.room.pk,
        )
        self.room.refresh_from_db()
        self.assertEqual(self.room.occupied_count, 1)
        self.assertEqual(
            Allocation.objects.filter(
                room=self.room,
                status=Allocation.Status.ACTIVE,
            ).count(),
            self.room.occupied_count,
        )

        AllocationService.vacate_room(student.pk)
        allocation.refresh_from_db()
        self.room.refresh_from_db()
        self.assertEqual(allocation.status, Allocation.Status.VACATED)
        self.assertEqual(self.room.occupied_count, 0)
