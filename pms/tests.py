from django.test import TestCase, Client
from django.urls import reverse
from .models import Room, Room_type

class RoomAjaxSearchViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        room_types = [Room_type(name='Standard', price=100.0, max_guests=2), Room_type(name='Deluxe', price=200.0, max_guests=4), Room_type(name='Luxury', price=300.0, max_guests=6)]
        Room_type.objects.bulk_create(room_types)
        rooms = [Room(name='Room 1', room_type=room_types[0], description='First Room'),
                 Room(name='Room 2', room_type=room_types[1], description='Second Room'),
                 Room(name='Room 3', room_type=room_types[2], description='Third Room')]
        Room.objects.bulk_create(rooms)

    def test_search_view_with_valid_query(self):
        response = self.client.get(reverse('room_ajax_search'), {'query': 'Room 2'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Room 2')
        self.assertNotContains(response, 'Room 1')
        self.assertNotContains(response, 'Room 3')

    def test_search_view_with_invalid_query(self):
        response = self.client.get(reverse('room_ajax_search'), {'query': 'Invalid Room'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '')

    def test_search_view_without_query(self):
        response = self.client.get(reverse('room_ajax_search'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Room 1')
        self.assertContains(response, 'Room 2')
        self.assertContains(response, 'Room 3')

