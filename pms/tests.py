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

    def test_edit_date(self):
        """Testing edit booking date"""
        response = self.client.post(
                f'/booking/{self.booking.id}/edit_date',
                {'checkin': '2022-11-06', 'checkout': '2022-11-02'})
        self.assertEqual(response.status_code, 409)

        Booking.objects.create(
                state="NEW",
                checkin=datetime.datetime.strptime('2022-11-20', '%Y-%m-%d'),
                checkout=datetime.datetime.strptime('2022-11-26', '%Y-%m-%d'),
                room=self.simple_room_1, guests=1, customer=self.customer,
                total=1, code=1,
        )

        response = self.client.post(
                f'/booking/{self.booking.id}/edit_date',
                {'checkin': '2022-11-21', 'checkout': '2022-11-25'})
        self.assertEqual(response.status_code, 409)
        response = self.client.post(
                f'/booking/{self.booking.id}/edit_date',
                {'checkin': '2022-11-20', 'checkout': '2022-11-26'})
        self.assertEqual(response.status_code, 409)
        response = self.client.post(
                f'/booking/{self.booking.id}/edit_date',
                {'checkin': '2022-11-19', 'checkout': '2022-11-21'})
        self.assertEqual(response.status_code, 409)
        response = self.client.post(
                f'/booking/{self.booking.id}/edit_date',
                {'checkin': '2022-11-25', 'checkout': '2022-11-27'})
        self.assertEqual(response.status_code, 409)
        response = self.client.post(
                f'/booking/{self.booking.id}/edit_date',
                {'checkin': '2022-11-18', 'checkout': '2022-11-20'})
        self.assertEqual(response.status_code, 302)
        response = self.client.post(
                f'/booking/{self.booking.id}/edit_date',
                {'checkin': '2022-11-26', 'checkout': '2022-11-30'})
        self.assertEqual(response.status_code, 302)
