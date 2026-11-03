
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
        self.client.login(
            username="admin",
            password="Admin@123",
        )

        response = self.client.get(
            reverse("rooms:room_list")
        )

        self.assertEqual(response.status_code, 200)

    def test_non_admin_cannot_access_room_list(self):
        self.client.login(
            username="student",
            password="Student@123",
        )

        response = self.client.get(
            reverse("rooms:room_list")
        )

        self.assertEqual(response.status_code, 403)

    def test_admin_can_add_hostel(self):
        self.client.login(
            username="admin",
            password="Admin@123",
        )

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
        self.client.login(
            username="admin",
            password="Admin@123",
        )

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
        self.client.login(
            username="student",
            password="Student@123",
        )

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
        self.client.login(
            username="admin",
            password="Admin@123",
        )

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

        self.client.login(
            username="admin",
            password="Admin@123",
        )

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
        self.client.login(
            username="admin",
            password="Admin@123",
        )

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
        self.client.login(
            username="student",
            password="Student@123",
        )

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

    def test_available_beds_calculation(self):
        room = Room.objects.create(
            hostel=self.hostel,
            room_number="104",
            capacity=5,
            occupied_count=2,
        )

        self.assertEqual(room.available_beds, 3)
