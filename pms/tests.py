from django.test import TestCase
from django.urls import reverse
from .models import Customer, Room_type, Room, Booking


class DashboardViewTestCase(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(name="Test Customer", email="test@example.com", phone="1234567890")
        self.room_type = Room_type.objects.create(name="Test Room Type", price=100.0, max_guests=2)
        self.room = Room.objects.create(room_type=self.room_type, name="Test Room", description="Test Room Description")
        self.room2 = Room.objects.create(room_type=self.room_type, name="Test Room 2", description="Test Room Description 2")
        self.booking = Booking.objects.create(state="NEW", checkin="2023-10-17", checkout="2023-10-19",
                                              room=self.room, guests=2, customer=self.customer, total=200.0, code="TEST123")
    def test_dashboard_view(self):
        url = reverse('dashboard') 
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_dashboard_data(self):
        url = reverse('dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        dashboard = response.context['dashboard']

        self.assertContains(response, "Reservas hechas")
        self.assertContains(response, "Huéspedes ingresando")
        self.assertContains(response, "Huéspedes saliendo")
        self.assertContains(response, "% ocupación")
        self.assertContains(response, "Total facturado")
        self.assertEqual(dashboard['new_bookings'], 1)
        self.assertEqual(dashboard['incoming_guests'], 1)
        self.assertEqual(dashboard['outcoming_guests'], 0)
        self.assertEqual(dashboard['occupancy'], 50.0)
        self.assertEqual(dashboard['invoiced']['total__sum'], 200.0)

