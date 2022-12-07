from datetime import date, timedelta

import django
from django.test import TestCase
from django.urls import reverse
django.setup()

from pms.models import Booking, Room


class TestDashboardView(TestCase):
    """ Test Dashboard View"""
    
    def setUp(self):
        self.today = date.today()
        self.room_1 = Room.objects.get(name='Room 1.1')
        self.room_2 = Room.objects.get(name='Room 2.1')
        
        self.booking_1 = Booking.objects.create(
            checkin=self.today - timedelta(days=1),
            checkout=self.today + timedelta(days=2),
            room_id=self.room_1.id,
            guests=1,
            total=(self.room_1.room_type.price)*4,
            code='SD45G678'
        )

        self.booking_2 = Booking.objects.create(
            checkin=self.today - timedelta(days=2),
            checkout=self.today + timedelta(days=4),
            room_id=self.room_2.id,
            guests=2,
            total=(self.room_1.room_type.price)*7,
            code='HOJ87LPR'
        )      
    
    def test_occupancy(self):
        """ Check the occupancy percentage value"""

        confirmed_bookings = Booking.objects.filter(
            state="NEW",
            checkout__gte=self.today,
        ).count()
        occupancy = f"{(confirmed_bookings / Room.objects.count())*100} %"
        response = self.client.get(reverse('dashboard'))
        content = str(response.content)
    
        self.assertEqual(response.status_code, 200)
        self.assertIn(occupancy,  content)
