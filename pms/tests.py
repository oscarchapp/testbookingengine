from django.test import TestCase

from django.urls import reverse
from .models import Room, Room_type

# Create your tests here.

class RoomsViewTest(TestCase):
    def setUp(self):
        self.room_single_type = Room_type.objects.create(name='Single', price=100, max_guests=1)
        self.room_double_type = Room_type.objects.create(name='Double', price=100, max_guests=1)
        self.room1 = Room.objects.create(room_type=self.room_single_type, name='1.1', description='Habitación individual')
        self.room2 = Room.objects.create(room_type=self.room_double_type, name='2.1', description='Habitación doble')

    def test_rooms_view(self):
        url = reverse('rooms')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        filtered_rooms = [str(room['name']) for room in response.context['filtered_rooms']]
        expected_reprs = [str(self.room1), str(self.room2)]
        
        self.assertEqual(filtered_rooms, expected_reprs)

    def test_rooms_view_with_filter(self):
        url = reverse('rooms') + '?filter_value=' + str(self.room1)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        filtered_rooms = [str(room['name']) for room in response.context['filtered_rooms']]
        expected_reprs = [str(self.room1)]
        
        self.assertEqual(filtered_rooms, expected_reprs)