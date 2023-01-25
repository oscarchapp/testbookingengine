from django.test import TestCase, override_settings
from django.urls import reverse
from django.test import Client
from pms.models import Room
from django.core import serializers
# Create your tests here.


class RoomsViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.rooms_url = reverse('rooms')



    def test_post_rooms_view(self):
        newRoom = Room()
        newRoom.name = 'Room 1.1'
        newRoom.save()
        newRoom2 = Room()
        newRoom2.name = 'Room 2.1'
        newRoom2.save()
        room1 = Room.objects.filter(name='Room 1.1').values("name", "room_type__name", "id")
        room2 = Room.objects.filter(name='Room 2.1').values("name", "room_type__name", "id")
        room_all = Room.objects.all().values("name", "room_type__name", "id")
        room_Filtered = Room.filter_rooms('Room 1')
        room_Filtered2 = Room.filter_rooms('Room 2')
        room_Filtered_all = Room.filter_rooms('Room')
        self.assertQuerysetEqual(room_Filtered, room1)
        self.assertQuerysetEqual(room_Filtered2, room2)
        self.assertQuerysetEqual(list(room_Filtered_all), list(room_all))

