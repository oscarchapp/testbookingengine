from django.test import Client, TestCase, override_settings

# Create your tests here.
from django.test import TestCase
from datetime import date, timedelta

from django.urls import reverse
from pms.models import Room, Booking
from pms.tests.factory import BookingFactory, RoomFactory
from django.contrib.messages import get_messages

_SFS ='django.contrib.staticfiles.storage.StaticFilesStorage'


@override_settings(STATICFILES_STORAGE=_SFS)
class BookingEditTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        today = date.today()
        cls.booking_room_1 = BookingFactory.create(
            state=Booking.NEW,
            checkin=today,
            checkout=today + timedelta(days=1),
            total=10
        )
        cls.booking_room_2 = BookingFactory.create(
            room=cls.booking_room_1.room,
            state=Booking.NEW,
            checkin=today + timedelta(days=2),
            checkout=today + timedelta(days=5),
            total=10
        )
        cls.URL = reverse(
            'edit_booking',
            args=[cls.booking_room_1.id]
        )

    def test_use_correct_template(self):
        """
        This test check that we are using the correct template
        """
        response = self.client.get(self.URL, {"type": "date_editing"})
        self.assertTemplateUsed(response, "edit_booking_date.html")

    def test_change_invalid_bookings_date(self):
        """
        This verify that a date that has already been taken cannot be occupied.
        Also verify that it doesn't redirect
        """
        today = date.today()
        response = self.client.post(
            path=f"{self.URL}?type=date_editing",
            data={
                "checkin": today + timedelta(days=1),
                "checkout": today + timedelta(days=2)
            },
            follow=True
        )
        self.assertTemplateUsed(response, "edit_booking_date.html")
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'No hay disponibilidad para las fechas seleccionadas.')

    def test_change_bookings_date(self):
        """
        This we check that the dates are modified correctly
        """
        today = date.today()
        checkin = today + timedelta(days=6)
        checkout = today + timedelta(days=7)
        response = self.client.post(
            path=f"{self.URL}?type=date_editing",
            data={
                "checkin": checkin,
                "checkout": checkout
            },
            follow=True
        )
        self.assertRedirects(response, "/", 302)
        self.assertTemplateUsed(response, "home.html")
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Fechas actualizadas correctamente.')
        self.assertTrue(
            Booking.objects.filter(
                id=self.booking_room_1.id,
                checkin=checkin,
                checkout=checkout
            ).exists()
        )
