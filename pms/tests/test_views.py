from django.test import TestCase, Client
from django.urls import reverse
from pms.models import Room, Room_type
import pdb


class RoomsViewTest(TestCase):
    # Initial setUp
    def setUp(self):
        self.client = Client()
        self.room_type = Room_type.objects.create(
            name="Single", max_guests=1, price=100
        )
        self.room1 = Room.objects.create(name="Room 101", room_type=self.room_type)
        self.room2 = Room.objects.create(name="Room 102", room_type=self.room_type)
        self.room3 = Room.objects.create(name="Suite 201", room_type=self.room_type)

    # Test for rooms view
    def test_rooms_view_without_search(self):
        response = self.client.get(reverse("rooms"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Room 101")
        self.assertContains(response, "Room 102")
        self.assertContains(response, "Suite 201")

    # Test for rooms view with search value
    def test_rooms_view_with_search(self):
        response = self.client.get(reverse("rooms"), {"search": "Room"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Room 101")
        self.assertContains(response, "Room 102")
        self.assertNotContains(response, "Suite 201")

    # Test for rooms view with search value that does not match any room
    def test_rooms_view_with_search_no_results(self):
        response = self.client.get(reverse("rooms"), {"search": "Nonexistent"})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Room 101")
        self.assertNotContains(response, "Room 102")
        self.assertNotContains(response, "Suite 201")
