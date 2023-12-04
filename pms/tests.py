from django.test import TestCase, Client
from django.urls import reverse

from .models import Room, Room_type


class SetUp(TestCase):

    def setUp(self):
        """
        Setup:
        - 2 room types(simple and double)
        - 4 rooms (1 simple, 3 doubles)
        """
        simple_room_type = Room_type.objects.create(name='Simple', price=20.0, max_guests=1)
        double_room_type = Room_type.objects.create(name='Double', price=30.0, max_guests=2)

        room_1_1 = Room.objects.create(room_type=simple_room_type, name='Room 1.1', description='Lorem Ipsum')
        room_2_1 = Room.objects.create(room_type=double_room_type, name='Room 2.1', description='Lorem Ipsum')
        room_2_2 = Room.objects.create(room_type=double_room_type, name='Room 2.2', description='Lorem Ipsum')
        room_2_3 = Room.objects.create(room_type=double_room_type, name='Room 2.3', description='Lorem Ipsum')


class TestRooms(SetUp):

    def test_room_name_filter_existing(self):

        """
        Testing filter rooms by name
        3 rooms where created including the name '2.' so it should return 3 results
        """
        search_data = {'room_name_filter': '2.'}

        response = self.client.post(reverse('rooms'), data=search_data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '3 resultados')


    def test_room_name_filter_non_existing(self):
        """
        Testing no existing rooms
        There are not rooms which name include '5.' so it should return 0 results.
        Same behaviour with any character with no results
        """
        search_data = {'room_name_filter': '5.'}

        response = self.client.post(reverse('rooms'), data=search_data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '0 resultados')

    def test_room_name_filter_invalid_param(self):
        """
        Testing invalid search param
        Searching with wrong param 'room_name_filters'
        """
        search_data = {'room_name_filters': '5.'}

        response = self.client.post(reverse('rooms'), data=search_data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ocurrió un error al intentar filtrar las habitaciones')
