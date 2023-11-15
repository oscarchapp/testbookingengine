from datetime import date, timedelta

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages

from .models import Room, Room_type, Booking
from .forms import EditDatesForm


class EditBookingDateViewTests(TestCase):
    def setUp(self):
        room_type = Room_type.objects.create(name="Double", price=100.0, max_guests=2)
        self.room = Room.objects.create(room_type=room_type, name="Sample Room", description="Test Room")
        self.booking = Booking.objects.create(
            room=self.room,
            checkin=date.today(),
            checkout=date.today() + timedelta(days=3),
            guests=2,
            total=300.0,
            code="TEST123",
            created=date.today()
        )

        self.edit_dates_form_data = {
            "booking-checkin": date.today() + timedelta(days=1),
            "booking-checkout": date.today() + timedelta(days=4),
        }

        self.url = reverse('edit_booking_date', args=[self.booking.id])
        self.client = Client()

    def test_get_edit_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_get_validate_is_edition(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'booking_search_form.html')
        self.assertTrue(response.context['edit'])

    def test_get_validate_is_form_instance(self):
        response = self.client.get(self.url)
        self.assertIsInstance(response.context['form'], EditDatesForm)
        self.assertEqual(response.context['form'].prefix, 'booking')

    def test_get_nonexistent_booking_redirect(self):
        fake_booking_id = self.booking.id + 1
        fake_url = reverse('edit_booking_date', args=[fake_booking_id])
        response = self.client.get(fake_url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

    def test_get_nonexistent_booking_message(self):
        fake_booking_id = self.booking.id + 1
        fake_url = reverse('edit_booking_date', args=[fake_booking_id])
        response = self.client.get(fake_url)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Booking does not exist")

    def test_valid_form_data(self):
        response = self.client.post(
            self.url,
            self.edit_dates_form_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")
        self.assertEqual(
            Booking.objects.get(id=self.booking.id).checkin,
            self.edit_dates_form_data["booking-checkin"],
        )
        self.assertEqual(
            Booking.objects.get(id=self.booking.id).checkout,
            self.edit_dates_form_data["booking-checkout"],
        )

    def test_date_updated_correctly(self):
        response = self.client.post(
            self.url,
            self.edit_dates_form_data
        )
        self.assertEqual(response.status_code, 302)

        response = self.client.get("/")
        self.assertContains(response, "Fechas actualizadas correctamente.")

    def test_room_unavailable(self):
        response = self.client.post(
            self.url,
            self.edit_dates_form_data,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertContains(
            response, "No hay disponibilidad para las fechas seleccionadas."
        )
