from datetime import date, timedelta

import django
from django.test import TestCase
from django.urls import reverse
django.setup()

from pms.models import Booking, Room


class TestRoomsView(TestCase):
    """ Test Rooms View"""
    
    def setUp(self):
        self.room_1 = Room.objects.get(name='Room 1.1')
        self.room_2 = Room.objects.get(name='Room 2.1')
        self.room_3 = Room.objects.get(name='Room 2.2')

    def test_room_list(self):
        """ Check that all rooms are listed"""

        response = self.client.get(reverse('rooms'))
        content = str(response.content)
    
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.room_1.name, content)
        self.assertIn(self.room_2.name, content)
        self.assertIn(self.room_3.name, content)

    def test_room_search_name(self):
        """ Check that the search by name filter correctly"""

        response = self.client.get('%s?name=%s' % (reverse('rooms'), 'Room 1'))
        content = str(response.content)
    
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.room_1.name, content)
        self.assertNotIn(self.room_2.name, content)
        self.assertNotIn(self.room_3.name, content)
