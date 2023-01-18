from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Booking, Customer, Room, Room_type

class EditDatesViewTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            name='John Doe', email='johndoe@example.com', phone='555-555-5555'
        )
        self.room_type = Room_type.objects.create(
            name='Single Room', price=100, max_guests=1
        )
        self.room = Room.objects.create(
            room_type=self.room_type, name='Room 101', description='Nice room'
        )
        self.booking = Booking.objects.create(
            checkin=timezone.now(), checkout=timezone.now() + timezone.timedelta(days=1),
            room=self.room, guests=1, customer=self.customer, total=100, code='ABCDEFGH'
        )

    
    def test_edit_dates_view_get(self):
        # Test GET request
        response = self.client.get(reverse('edit_dates', args=[self.booking.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_reservation_dates.html')

    def test_edit_dates_view_post_valid(self):
        # Test POST request with valid data
        checkin = timezone.now()
        checkout = checkin + timezone.timedelta(days=1)
        response = self.client.post(reverse('edit_dates', args=[self.booking.pk]), {
            'checkin': checkin.strftime('%Y-%m-%d'),
            'checkout': checkout.strftime('%Y-%m-%d'),
        })
        self.assertRedirects(response, reverse('room_details', args=[self.room.pk]))

    def test_edit_dates_view_post_invalid(self):
        # Test POST request with invalid data
        checkin = timezone.now() + timezone.timedelta(days=1)
        checkout = timezone.now()
        response = self.client.post(reverse('edit_dates', args=[self.booking.pk]), {
        'checkin': checkin.strftime('%Y-%m-%d'),
        'checkout': checkout.strftime('%Y-%m-%d'),
        })
        self.assertNotEqual(response.status_code, 200)

    def test_edit_dates_view_post_not_available(self):
        # Test POST request with not available dates
        checkin = timezone.now()
        checkout = checkin + timezone.timedelta(days=1)
        # Create another booking with the same room but different dates
        Booking.objects.create(
            room=self.booking.room,
            checkin=checkin,
            checkout=checkout,
            guests=1,
            customer=self.customer,
            total=100
        )
        response = self.client.post(reverse('edit_dates', args=[self.booking.pk]), {
            'checkin': checkin.strftime('%Y-%m-%d'),
            'checkout': checkout.strftime('%Y-%m-%d'),
        })
        self.assertContains(response, 'No hay disponibilidad para las fechas seleccionadas')       