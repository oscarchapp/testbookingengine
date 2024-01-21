from django.test import TestCase, RequestFactory
from django.urls import reverse
from pms.views import RoomsView
from pms.models import Room, Room_type

class RoomsViewTestCase(TestCase):
    def setUp(self):
        room_type = Room_type.objects.create(name="Simple", price=100.0, max_guests=1)
        Room.objects.create(name="Room 1.1", room_type=room_type)
        Room.objects.create(name="Room 1.2", room_type=room_type)
        Room.objects.create(name="Room 2.1", room_type=room_type)

        self.factory = RequestFactory()
    
    def test_rooms_view_without_filter(self):
        url = reverse('rooms')
        request = self.factory.get(url)
        response = RoomsView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Room 1.1")
        self.assertContains(response, "Room 1.2")
        self.assertContains(response, "Room 2.1")

    def test_rooms_view_with_filter(self):
        url = reverse('rooms')
        request = self.factory.get(url, {'name': 'Room 1'})
        response = RoomsView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Room 1.1")
        self.assertContains(response, "Room 1.2")
        self.assertNotContains(response, "Room 2.1")

    def test_rooms_view_with_empty_filter(self):
        url = reverse('rooms')
        request = self.factory.get(url, {'name': ''})
        response = RoomsView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Room 1.1")
        self.assertContains(response, "Room 1.2")
        self.assertContains(response, "Room 2.1")