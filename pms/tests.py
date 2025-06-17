from django.test import TestCase
from django.urls import reverse
from .models import Room, Room_type

class RoomsViewTests(TestCase):
    def setUp(self):
        tipo1 = Room_type.objects.create(name='Tipo A')
        tipo2 = Room_type.objects.create(name='Tipo B')

        Room.objects.create(name='Room 1.1', room_type=tipo1)
        Room.objects.create(name='Room 1.2', room_type=tipo1)
        Room.objects.create(name='Room 2.1', room_type=tipo2)

    def test_ajax_search_filter(self):
        response = self.client.get(
            reverse('rooms'),
            {'search': 'Room 1'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn("Room 1.1", content)
        self.assertIn("Room 1.2", content)
        self.assertNotIn("Room 2.1", content)
