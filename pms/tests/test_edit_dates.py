from django.test import TestCase
from django.urls import reverse
from pms.models import Booking, Room, Room_type
from datetime import date

class EditBookingDatesViewTest(TestCase):
    # Set up the test
    def setUp(self):
        self.room_type = Room_type.objects.create(name="Single", price=100, max_guests=1)
        self.room = Room.objects.create(name="101", room_type=self.room_type)
        self.booking = Booking.objects.create(
            room=self.room,
            checkin=date(2025, 2, 24),
            checkout=date(2025, 2, 26),
            guests=1,
            state="NEW",
            customer=None,  # Default value to evade integrity errors
            total=0.0,
            code="ABC12345"
        )
        self.url = reverse('edit_booking_dates', args=[self.booking.id])
    
    # Test the GET request
    def test_edit_booking_dates_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_booking_dates.html')
    
    # Test the POST request with valid data
    def test_edit_booking_dates_view_post_valid(self):
        data = {
            'booking-checkin': '2025-02-25',
            'booking-checkout': '2025-02-27'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.checkin, date(2025, 2, 25))
        self.assertEqual(self.booking.checkout, date(2025, 2, 27))

    # Test the POST request with invalid data
    def test_edit_booking_dates_view_post_invalid(self):
        # Create an overlapping booking
        Booking.objects.create(
            room=self.room,
            checkin=date(2025, 2, 25),
            checkout=date(2025, 2, 27),
            guests=1,
            state="NEW",
            customer=None,  # Default value to evade integrity errors
            total=0.0,
            code="DEF67890"
        )
        data = {
            'booking-checkin': '2025-02-25',
            'booking-checkout': '2025-02-27'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No hay disponibilidad para las fechas seleccionadas")