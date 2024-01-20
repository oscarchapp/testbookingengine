from django.test import TestCase, RequestFactory
from django.urls import reverse

from datetime import date, timedelta
from pms.models import Booking, Room, Room_type, Customer
from pms.views import DashboardView

class DashboardViewGetTest(TestCase):
    def setUp(self):
        # Create rooms and customer
        room_type = Room_type.objects.create(name='Single', 
                                             price=50.0, 
                                             max_guests=1)
        room = Room.objects.create(room_type=room_type, 
                                   name='Room 1.1', 
                                   description='Single Room')
        customer = Customer.objects.create(name='Dharma Alisum', 
                                           email='dharma@test.com', 
                                           phone='123456789')

        # Booking for today
        Booking.objects.create(state='NEW', 
                               checkin=date.today(), 
                               checkout=date.today() + timedelta(days=1), 
                               room=room, 
                               guests=1, 
                               customer=customer, 
                               total=50.0, 
                               code='ABC123')

        # Booking for today with different room_type
        room_type2 = Room_type.objects.create(name='Double', price=70.0, max_guests=2)
        room2 = Room.objects.create(room_type=room_type2, name='Room 2.1', description='Double Room')
        Booking.objects.create(state='NEW', 
                               checkin=date.today(), 
                               checkout=date.today()+ timedelta(days=1), 
                               room=room2, 
                               guests=2, 
                               customer=customer, 
                               total=70.0, 
                               code='XYZ789')
        # Booking for tomorrow
        room_type3 = Room_type.objects.create(name='Triple', price=90.0, max_guests=3)
        room3 = Room.objects.create(room_type=room_type3, name='Room 3.1', description='Triple Room')
        Booking.objects.create(state='NEW', 
                               checkin=date.today()+ timedelta(days=1), 
                               checkout=date.today()+ timedelta(days=3), 
                               room=room3, 
                               guests=3, 
                               customer=customer, 
                               total=180.0, 
                               code='WER789')

    def test_get_method(self):

        # request with client
        response = self.client.get(reverse('dashboard'))

        # response verify
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<h1>Dashboard</h1>')
        self.assertContains(response, '% Ocupación')

        # context of response
        dashboard_data = response.context['dashboard']

        # Dashboard values 
        self.assertEqual(dashboard_data['new_bookings'], 3)  
        self.assertEqual(dashboard_data['incoming_guests'], 2)  
        self.assertEqual(dashboard_data['outcoming_guests'], 0)  
        self.assertEqual(dashboard_data['invoiced'], {'total__sum': 300})  
        self.assertEqual(dashboard_data['occupancy'], 100.0)  

