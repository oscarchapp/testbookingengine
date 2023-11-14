from django.test import TestCase, Client
from django.urls import reverse

from .models import Room, Room_type


class RoomsViewTests(TestCase):
    def setUp(self):
        # Set up test data
        self.room_type = Room_type.objects.create(
            name="Single", price=50.0, max_guests=1
        )
        self.room = Room.objects.create(
            room_type=self.room_type, name="Room 101"
        )
        self.client = Client()

    def test_get_request(self):
        response = self.client.get(reverse('rooms'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Room 101")

    def test_post_request_with_invalid_room_name(self):
        response = self.client.post(
            reverse('rooms'), data={'room_name': 'Invalid Room'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No rooms for Invalid Room pattern.")

    def test_post_request_with_valid_room_name(self):
        response = self.client.post(
            reverse('rooms'), data={'room_name': 'Room 101'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Room 101")
