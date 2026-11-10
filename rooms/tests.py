
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Hostel, Room


class HostelRoomManagementTests(TestCase):

    def setUp(self):
        self.admin = User.objects.create_user(
            username="admin",
            password="Admin@123",
            is_staff=True,
        )

        self.student = User.objects.create_user(
            username="student",
            password="Student@123",
            is_staff=False,
        )

        self.hostel = Hostel.objects.create(
            name="Test Hostel",
            block="A Block",
        )

    def test_admin_can_access_room_list(self):
        self.client.force_login(self.admin)

        response = self.client.get(
            reverse("rooms:room_list")
        )

        self.assertEqual(response.status_code, 200)

    def test_non_admin_cannot_access_room_list(self):
        self.client.force_login(self.student)

        response = self.client.get(
            reverse("rooms:room_list")
        )

        self.assertEqual(response.status_code, 403)

    def test_admin_can_add_hostel(self):
        self.client.force_login(self.admin)

        response = self.client.post(
            reverse("rooms:hostel_add"),
            {
                "name": "New Hostel",
                "block": "B Block",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Hostel.objects.filter(name="New Hostel").exists()
        )

    def test_duplicate_hostel_is_rejected(self):
        self.client.force_login(self.admin)

        response = self.client.post(
            reverse("rooms:hostel_add"),
            {
                "name": "Test Hostel",
                "block": "C Block",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Hostel.objects.filter(name__iexact="Test Hostel").count(),
            1,
        )

    def test_non_admin_cannot_add_hostel(self):
        self.client.force_login(self.student)

        response = self.client.post(
            reverse("rooms:hostel_add"),
            {
                "name": "Unauthorized Hostel",
                "block": "D Block",
            },
        )

        self.assertEqual(response.status_code, 403)
        self.assertFalse(
            Hostel.objects.filter(
                name="Unauthorized Hostel"
            ).exists()
        )

    def test_admin_can_add_room(self):
        self.client.force_login(self.admin)

        response = self.client.post(
            reverse("rooms:room_add"),
            {
                "hostel": self.hostel.id,
                "room_number": "101",
                "capacity": 4,
            },
        )

        self.assertEqual(response.status_code, 302)

        room = Room.objects.get(
            hostel=self.hostel,
            room_number="101",
        )

        self.assertEqual(room.capacity, 4)
        self.assertEqual(room.occupied_count, 0)

    def test_duplicate_room_number_is_rejected(self):
        Room.objects.create(
            hostel=self.hostel,
            room_number="101",
            capacity=4,
        )

        self.client.force_login(self.admin)

        response = self.client.post(
            reverse("rooms:room_add"),
            {
                "hostel": self.hostel.id,
                "room_number": "101",
                "capacity": 3,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Room.objects.filter(
                hostel=self.hostel,
                room_number="101",
            ).count(),
            1,
        )

    def test_zero_room_capacity_is_rejected(self):
        self.client.force_login(self.admin)

        response = self.client.post(
            reverse("rooms:room_add"),
            {
                "hostel": self.hostel.id,
                "room_number": "102",
                "capacity": 0,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            Room.objects.filter(
                hostel=self.hostel,
                room_number="102",
            ).exists()
        )


    def test_non_admin_cannot_add_room(self):
        self.client.force_login(self.student)

        response = self.client.post(
            reverse("rooms:room_add"),
            {
                "hostel": self.hostel.id,
                "room_number": "103",
                "capacity": 4,
            },
        )

        self.assertEqual(response.status_code, 403)
        self.assertFalse(
            Room.objects.filter(room_number="103").exists()
        )

    # HOSTEL-37: Room editing access control

    def test_admin_can_edit_room(self):
        room = Room.objects.create(
            hostel=self.hostel,
            room_number="105",
            capacity=4,
        )

        self.client.force_login(self.admin)

        response = self.client.get(
            reverse("rooms:room_edit", args=[room.id])
        )

        self.assertEqual(response.status_code, 200)

    def test_non_admin_cannot_access_edit_room(self):
        room = Room.objects.create(
            hostel=self.hostel,
            room_number="106",
            capacity=4,
        )

        self.client.force_login(self.student)

        response = self.client.get(
            reverse("rooms:room_edit", args=[room.id])
        )

        self.assertEqual(response.status_code, 403)

    def test_non_admin_cannot_edit_room_using_post(self):
        room = Room.objects.create(
            hostel=self.hostel,
            room_number="107",
            capacity=4,
        )

        self.client.force_login(self.student)

        response = self.client.post(
            reverse("rooms:room_edit", args=[room.id]),
            {
                "hostel": self.hostel.id,
                "room_number": "108",
                "capacity": 6,
            },
        )

        self.assertEqual(response.status_code, 403)

        room.refresh_from_db()

        self.assertEqual(room.room_number, "107")
        self.assertEqual(room.capacity, 4)

    def test_available_beds_calculation(self):
        room = Room.objects.create(
            hostel=self.hostel,
            room_number="104",
            capacity=5,
            occupied_count=2,
        )

        self.assertEqual(room.available_beds, 3)


class RoomAvailabilityAndDetailsTests(TestCase):

    def setUp(self):
        self.admin = User.objects.create_user(
            username="room_admin",
            password="Admin@123",
            is_staff=True,
        )

        self.student = User.objects.create_user(
            username="room_student",
            password="Student@123",
            is_staff=False,
        )

        self.hostel_a = Hostel.objects.create(
            name="Hostel A",
            block="A Block",
        )

        self.hostel_b = Hostel.objects.create(
            name="Hostel B",
            block="B Block",
        )

        self.empty_room = Room.objects.create(
            hostel=self.hostel_a,
            room_number="101",
            capacity=4,
            occupied_count=0,
        )

        self.partial_room = Room.objects.create(
            hostel=self.hostel_a,
            room_number="102",
            capacity=4,
            occupied_count=2,
        )

        self.full_room = Room.objects.create(
            hostel=self.hostel_a,
            room_number="103",
            capacity=2,
            occupied_count=2,
        )

        self.other_hostel_room = Room.objects.create(
            hostel=self.hostel_b,
            room_number="201",
            capacity=3,
            occupied_count=1,
        )

        self.client.force_login(self.admin)

    def test_available_rooms_include_empty_and_partially_occupied(self):
        response = self.client.get(
            reverse("rooms:available_rooms")
        )

        self.assertEqual(response.status_code, 200)

        rooms = list(response.context["rooms"])

        self.assertIn(self.empty_room, rooms)
        self.assertIn(self.partial_room, rooms)
        self.assertIn(self.other_hostel_room, rooms)
        self.assertNotIn(self.full_room, rooms)

    def test_occupied_rooms_include_partially_occupied_and_full(self):
        response = self.client.get(
            reverse("rooms:occupied_rooms")
        )

        self.assertEqual(response.status_code, 200)

        rooms = list(response.context["rooms"])

        self.assertNotIn(self.empty_room, rooms)
        self.assertIn(self.partial_room, rooms)
        self.assertIn(self.full_room, rooms)
        self.assertIn(self.other_hostel_room, rooms)

    def test_available_rooms_can_be_filtered_by_hostel(self):
        response = self.client.get(
            reverse("rooms:available_rooms"),
            {"hostel": self.hostel_a.id},
        )

        self.assertEqual(response.status_code, 200)

        rooms = list(response.context["rooms"])

        self.assertIn(self.empty_room, rooms)
        self.assertIn(self.partial_room, rooms)
        self.assertNotIn(self.full_room, rooms)
        self.assertNotIn(self.other_hostel_room, rooms)

    def test_occupied_rooms_can_be_filtered_by_hostel(self):
        response = self.client.get(
            reverse("rooms:occupied_rooms"),
            {"hostel": self.hostel_a.id},
        )

        self.assertEqual(response.status_code, 200)

        rooms = list(response.context["rooms"])

        self.assertNotIn(self.empty_room, rooms)
        self.assertIn(self.partial_room, rooms)
        self.assertIn(self.full_room, rooms)
        self.assertNotIn(self.other_hostel_room, rooms)

    def test_room_details_display_correct_information(self):
        response = self.client.get(
            reverse(
                "rooms:room_detail",
                args=[self.partial_room.id],
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["room"],
            self.partial_room,
        )

        self.assertContains(response, "Hostel A")
        self.assertContains(response, "A Block")
        self.assertContains(response, "102")
        self.assertContains(response, "4")
        self.assertContains(response, "2")

        self.assertContains(response, "Available Beds")
        self.assertContains(response, "<td>2</td>", html=True)

        self.assertEqual(self.partial_room.available_beds, 2)

    def test_non_admin_cannot_view_available_rooms(self):
        self.client.force_login(self.student)

        response = self.client.get(
            reverse("rooms:available_rooms")
        )

        self.assertEqual(response.status_code, 403)

    def test_non_admin_cannot_view_occupied_rooms(self):
        self.client.force_login(self.student)

        response = self.client.get(
            reverse("rooms:occupied_rooms")
        )

        self.assertEqual(response.status_code, 403)

    def test_non_admin_cannot_view_room_details(self):
        self.client.force_login(self.student)

        response = self.client.get(
            reverse(
                "rooms:room_detail",
                args=[self.partial_room.id],
            )
        )

        self.assertEqual(response.status_code, 403)

    def test_nonexistent_room_details_return_404(self):
        response = self.client.get(
            reverse("rooms:room_detail", args=[99999])
        )

        self.assertEqual(response.status_code, 404)

    def test_available_rooms_show_empty_result_message(self):
        response = self.client.get(
            reverse("rooms:available_rooms"),
            {"hostel": "99999"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No available rooms found")

    def test_occupied_rooms_show_empty_result_message(self):
        response = self.client.get(
            reverse("rooms:occupied_rooms"),
            {"hostel": "99999"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "No occupied rooms found for the selected hostel.",
        )
