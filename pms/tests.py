import random

from django.test import TestCase, override_settings
from django.urls import reverse
from django.test import Client
from pms.models import Room, Booking
from django.core import serializers
# Create your tests here.
from .forms import BookingForm, CustomerForm

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


class PercentageBookedTest(TestCase):

    def setUp(self):
        from datetime import date
        self.client = Client()
        self.year = date.today().strftime("%Y")
        self.month = date.today().strftime("%m")
        self.day = date.today().strftime("%d")


    def test_percentage_rooms_booked(self):

        for index in range(10):
            newRoom = Room()
            newRoom.name = 'Room {}'.format(index)
            newRoom.save()
        for index in range(1,int(self.day)):
            newBooking = Booking()
            newBooking.total = '30'
            newBooking.checkin = '{}-{}-{}'.format(self.year,self.month, index)
            newBooking.checkout = '{}-{}-{}'.format(self.year,self.month, index+1)
            newBooking.guests = '3'
            newBooking.save()

        percentage = Booking()
        self.assertEqual(percentage.percentage_usage(), '0.10')


    def test_percentage_rooms_booked_Fail(self):

        for index in range(10):
            newRoom = Room()
            newRoom.name = 'Room {}'.format(index)
            newRoom.save()
        for index in range(1,int(self.day)):
            newBooking = Booking()
            newBooking.total = '30'
            newBooking.checkin = '{}-{}-{}'.format(self.year,self.month, index)
            newBooking.checkout = '{}-{}-{}'.format(self.year,self.month, index+5)
            newBooking.guests = '3'
            newBooking.save()

        percentage = Booking()
        self.assertNotEqual(percentage.percentage_usage(), '0.10')



