import datetime
from datetime import date

from django.test import TestCase, Client

from pms.models import Booking, Room, Customer, Room_type


class BookingTestCase(TestCase):
    client = Client()

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

        self.customer = Customer.objects.create(
                name="Jesus", email="jesus@chapp.com", phone="666555444"
        )

        self.booking = Booking.objects.create(
                state="NEW", checkin=date.today() - datetime.timedelta(days=1),
                checkout=date.today() + datetime.timedelta(days=2),
                room=self.simple_room_1, guests=1, customer=self.customer,
                total=1, code=1
        )

    def test_occupation(self):
        """Testing occupation percentage"""
        response = self.client.get('/dashboard/')
        self.assertEqual(response.context['dashboard']['occupation'], 25.0)
        Booking.objects.create(
                state="NEW", checkin=date.today() - datetime.timedelta(days=1),
                checkout=date.today() + datetime.timedelta(days=2),
                room=self.simple_room_2, guests=1, customer=self.customer,
                total=1, code=1,
        )
        response = self.client.get('/dashboard/')
        self.assertEqual(response.context['dashboard']['occupation'], 50.0)

        Booking.objects.create(
                state="DEL", checkin=date.today() - datetime.timedelta(days=1),
                checkout=date.today() + datetime.timedelta(days=2),
                room=self.simple_room_2, guests=1, customer=self.customer,
                total=1, code=1,
        )
        response = self.client.get('/dashboard/')
        self.assertEqual(response.context['dashboard']['occupation'], 50.0)

        Booking.objects.create(
                state="NEW", checkin=date.today() - datetime.timedelta(days=5),
                checkout=date.today(), room=self.doble_room_1, guests=1,
                customer=self.customer, total=1, code=1,
        )
        response = self.client.get('/dashboard/')
        self.assertEqual(response.context['dashboard']['occupation'], 75.0)

        Booking.objects.create(
                state="NEW",
                checkin=date.today() + datetime.timedelta(days=5),
                checkout=date.today() + datetime.timedelta(days=10),
                room=self.doble_room_2, guests=1, customer=self.customer,
                total=1, code=1,
        )
        response = self.client.get('/dashboard/')
        self.assertEqual(response.context['dashboard']['occupation'], 75.0)
