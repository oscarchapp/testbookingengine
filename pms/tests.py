from django.test import TestCase, Client
from pms.models import Room


class RoomsViewTest(TestCase):
    def setUp(self):
        rooms = [
            Room(
                name='room 1.1',
                description='Room description test'
            ),
            Room(
                name='room 2',
                description='Room description test'
            ),
            Room(
                name='room 2.2',
                description='Room description test'
            )
        ]
        Room.objects.bulk_create(rooms)
        self.client = Client()

    def test_search_name_room(self):
        data = {'name': 'room 1'}
        res = self.client.post('/rooms/', data)
        self.assertEqual(len(res.context['rooms']), 1)
        self.assertEqual(res.status_code, 200)
