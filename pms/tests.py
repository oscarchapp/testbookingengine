from datetime import date, datetime, timedelta
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.db.models import Sum

from .models import Room, Booking, Customer
from .views import DashboardView


class DashboardViewTests(TestCase):
    def setUp(self):
        room = Room.objects.create(
            name="Test Room", description="Test Description"
        )
        customer = Customer.objects.create(
            name="Test Customer", email="test@example.com", phone="123456789"
        )
        Booking.objects.create(
            state=Booking.NEW,
            checkin=date.today(),
            checkout=date.today() + timedelta(days=1),
            room=room,
            guests=2,
            customer=customer,
            total=100.0,
            code="ABC123",
            created=datetime.now()
        )

    def test_get_percentage_occupation(self):
        view = DashboardView()
        today = date.today()

        percentage = view.get_percentage_occupation(today)
        self.assertEqual(percentage, 100.0)

    def test_get_new_bookings(self):
        view = DashboardView()
        today = date.today()

        new_bookings = view.get_new_bookings(today)
        self.assertEqual(new_bookings, 1)

    def test_get_incoming_guests(self):
        view = DashboardView()
        today = date.today()

        incoming_guests = view.get_incoming_guests(today)
        self.assertEqual(incoming_guests, 1)

    def test_get_request(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_get_dashboard_data(self):
        response = self.client.get(reverse('dashboard'))
        self.assertIn('dashboard', response.context)
        dashboard_data = response.context['dashboard']
        self.assertEqual(dashboard_data['new_bookings'], 1)
        self.assertEqual(dashboard_data['incoming_guests'], 1)
