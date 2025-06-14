# en pms/tests.py
from django.test import TestCase, override_settings
from django.urls import reverse
from .models import Room_type, Room, Booking

@override_settings(
    STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage'
)
class RoomFilterTests(TestCase):
    def setUp(self):
        rt = Room_type.objects.create(name="Single", price=20, max_guests=1)
        Room.objects.create(name="Room 1.1", room_type=rt, description="")
        Room.objects.create(name="Deluxe Room 1.2", room_type=rt, description="")
        Room.objects.create(name="Room 2.1", room_type=rt, description="")

    def test_filter_rooms_by_name(self):
        url = reverse("rooms")
        response = self.client.get(url, {"filter": "Room 1"})
        self.assertEqual(response.status_code, 200)
        names = [r["name"] for r in response.context["rooms"]]
        self.assertIn("Room 1.1", names)
        self.assertIn("Deluxe Room 1.2", names)
        self.assertNotIn("Room 2.1", names)

@override_settings(
    STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage'
)
class DashboardOccupancyTests(TestCase):

    def setUp(self):
        # Creo 4 habitaciones
        rt = Room_type.objects.create(name="Test", price=10, max_guests=2)
        for i in range(4):
            Room.objects.create(name=f"Room {i+1}", room_type=rt, description="")

        # Creo 3 reservas en estado NEW
        rooms = list(Room.objects.all())
        for room in rooms[:3]:
            Booking.objects.create(
                state=Booking.NEW,
                checkin="2025-06-10",
                checkout="2025-06-12",
                room=room,
                guests=1,
                customer=None,
                total=20,
                code=f"CODE{i}"
            )

    def test_occupancy_percentage_context(self):
        url = reverse("dashboard")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        pct = response.context["dashboard"]["occupancy_pct"]
        # 3 reservas / 4 habitaciones = 75.0%
        self.assertEqual(pct, 75.0)