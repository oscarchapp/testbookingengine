from django.test import TestCase

from django.urls import reverse
from datetime import date, timedelta
from .models import Room, Booking, Customer, Room_type
from .views import DashboardView

# Create your tests here.


class DashboardViewTest(TestCase):
    def setUp(self):
        self.room_type = Room_type.objects.create(name='Single', price=100, max_guests=1)
        self.room = Room.objects.create(room_type=self.room_type, name='1.1', description='Habitación individual')
        self.customer = Customer.objects.create(name='Test Customer', email='customer@mail.com', phone='123456789')
        self.booking = Booking.objects.create(
            state=Booking.NEW,
            checkin=date.today(),
            checkout=date.today() + timedelta(days=2),
            room=self.room,
            guests=1,
            customer=self.customer,
            total=200,
            code='ABC123'
        )

    def test_dashboard_view(self):

        response = self.client.get(reverse('dashboard'))
        
        self.assertEqual(response.status_code, 200)

        dashboard_data = response.context['dashboard']
        
        self.assertEqual(dashboard_data['new_bookings'], 1)
        self.assertEqual(dashboard_data['incoming_guests'], self.booking.guests)
        self.assertEqual(dashboard_data['outcoming_guests'], 0)
        self.assertEqual(dashboard_data['invoiced']['total__sum'], self.booking.total)
        self.assertEqual(dashboard_data['occupation_percentage'], 100)
