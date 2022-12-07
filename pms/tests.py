from datetime import date, timedelta

import django
from django.test import TestCase
from django.urls import reverse
django.setup()

from pms.models import Booking, Room


class TestBookingDatesView(TestCase):
    """ Test Booking Dates View"""
    
    def setUp(self):
        self.today = date.today()
        self.room_1 = Room.objects.get(name='Room 1.3')
        
        self.booking_1 = Booking.objects.create(
            checkin=self.today - timedelta(days=1),
            checkout=self.today + timedelta(days=2),
            room_id=self.room_1.id,
            guests=1,
            total=(self.room_1.room_type.price)*4,
            code='GT45P948'
        )
    
    def test_detail_booking_dates(self):
        """ Check view to edit booking dates"""

        response = self.client.get(reverse('edit_dates', kwargs={'pk': self.booking_1.id}))
        content = str(response.content)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(str(self.booking_1.checkin), content)
        self.assertIn(str(self.booking_1.checkout), content)
        self.assertNotIn(str(self.booking_1.room.name), content)

    def test_edit_booking_dates(self):
        """ Validate the reservation date is updated """

        new_checkin =  self.today - timedelta(days=2)
        new_checkout = self.today + timedelta(days=3)
        data = {
            'checkin': new_checkin,
            'checkout': new_checkout
        }
        self.client.post(reverse('edit_dates', kwargs={'pk': self.booking_1.id}), data)
        
        self.booking_1.refresh_from_db()
        self.assertEqual(self.booking_1.checkin, new_checkin)
        self.assertEqual(self.booking_1.checkout, new_checkout)


    def test_fail_edit_booking_dates(self):
        """ Validate the reservation date is not updated """

        new_checkin =  self.today + timedelta(days=4)
        new_checkout = self.today + timedelta(days=6)

        Booking.objects.create(
            checkin=new_checkin,
            checkout=self.today + timedelta(days=7),
            room_id=self.room_1.id,
            guests=1,
            total=(self.room_1.room_type.price)*4,
            code='SW45P948'
        )

        data = {
            'checkin': new_checkin,
            'checkout': new_checkout
        }
        response = self.client.post(
            reverse('edit_dates', kwargs={'pk': self.booking_1.id}),
            data,
            follow=True
        )
        content = str(response.content)

        self.assertIn('No hay disponibilidad para las fechas seleccionadas', content)