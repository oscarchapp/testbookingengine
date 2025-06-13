# en pms/tests.py
from django.test import TestCase, override_settings
from django.urls import reverse
from .models import Room_type, Room

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
