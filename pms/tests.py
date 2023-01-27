import random

from django.test import TestCase, override_settings
from django.urls import reverse
from django.test import Client
from pms.models import Room, Booking, Customer
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
        for index in range(10):
            Room.objects.create(
                name='Room 1.{}'.format(index)
            )


    def test_percentage_rooms_booked(self):
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
        for index in range(1,int(self.day)):
            newBooking = Booking()
            newBooking.total = '30'
            newBooking.checkin = '{}-{}-{}'.format(self.year,self.month, index)
            newBooking.checkout = '{}-{}-{}'.format(self.year,self.month, index+5)
            newBooking.guests = '3'
            newBooking.save()

        percentage = Booking()
        self.assertNotEqual(percentage.percentage_usage(), '0.10')



class EditBookingDatesTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('edit_booking_dates',args=['1'])
        for index in range(5):
            room = Room.objects.create(
                name='Room 1.{}'.format(index)
            )
            customer = Customer.objects.create(
                name='XXX{}'.format(index)
            )
            Booking.objects.create(
                checkin='2023-02-08',
                checkout='2023-02-10',
                guests=2,
                state='NEW',
                total=150,
                customer_id =customer.id,
                room_id= room.id,
                code = 'XASDERD{}'.format(index)
            )
        for index in range(6):
            Room.objects.create(
                name='Room 2.{}'.format(index)
            )
    @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
    def test_edit_book_dates_get(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_booking_dates.html')

    @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
    def test_edit_book_dates_post(self):
        response = self.client.post(self.url,{
            'booking-checkin': '2023-02-09',
            'booking-checkout': '2023-02-12',
        })

        self.assertEquals(response.status_code, 302)
        self.assertEquals(Booking.objects.first().checkout.strftime("%Y-%m-%d"), '2023-02-12')

    @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
    def test_edit_book_dates_post_redirect(self):
        response = self.client.post(self.url,{
            'checkin': '2023-02-09',
            'checkout': '2023-02-12',
        })

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_booking_dates.html')
        self.assertEquals(Booking.objects.first().checkout.strftime("%Y-%m-%d"), '2023-02-10')

    @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
    def test_edit_book_dates_post_empty_redirect(self):
        response = self.client.post(self.url,{
            'booking-checkin': '',
            'booking-checkout': '2023-02-12',
        })

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_booking_dates.html')
        self.assertEquals(Booking.objects.first().checkout.strftime("%Y-%m-%d"), '2023-02-10')

    def test_verify_availability_ofchange(self):
        availability = Booking()
        data ={
            'checkin': '2023-02-01',
            'checkout': '2023-02-07',
            'code': 'OOF6AUTS',
            'guests': '2',
            'room_id': '11',
        }
        response = availability.verify_availability_ofchange(data)
        print(response)
