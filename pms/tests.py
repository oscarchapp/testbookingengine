from django.test import TestCase

from pms.models import Room, Room_type


class BookingTestCase(TestCase):

    def setUp(self):
        self.simple_room_type = Room_type.objects.create(
                name="Simple", price=20, max_guests=1
        )
        self.doble_room_type = Room_type.objects.create(
                name="Doble", price=30, max_guests=2
        )

        self.simple_room_1 = Room.objects.create(
                room_type=self.simple_room_type, name="Room 1.1",
                description="Habitación para una persona"
        )
        self.simple_room_2 = Room.objects.create(
                room_type=self.simple_room_type, name="Room 1.2",
                description="Habitación para una persona"
        )
        self.doble_room_1 = Room.objects.create(
                room_type=self.doble_room_type, name="Room 2.1",
                description="Habitación para dos personas"
        )
        self.doble_room_2 = Room.objects.create(
                room_type=self.doble_room_type, name="Room 2.1",
                description="Habitación para dos personas"
        )

    def test_room_filter(self):
        """Testing rooms filter"""
        response = self.client.get('/rooms/', {'name': 'room'})
        self.assertEqual(len(response.context['rooms'].qs), 4)
        response = self.client.get('/rooms/', {'name': 'room 1'})
        self.assertEqual(len(response.context['rooms'].qs), 2)
        response = self.client.get('/rooms/', {'name': 'room 1.1'})
        self.assertEqual(len(response.context['rooms'].qs), 1)
