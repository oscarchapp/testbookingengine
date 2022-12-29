from django.test import TestCase
from django.urls import reverse
from pms.models import Room, Room_type, Booking
from pms.forms import BookingEditDatesForm
from datetime import datetime

class BookingEditDatesViewTest(TestCase):

    def setUp(self):
        self.room_type_simple = Room_type.objects.create(
            name="Simple", price=20, max_guests=2
        )
        self.room_type_double = Room_type.objects.create(
            name="Doble", price=30, max_guests=2
        )
        self.room_type_triple = Room_type.objects.create(
            name="Triple", price=40, max_guests=3
        )
        self.room_type_quadruple = Room_type.objects.create(
            name="Cuadruple", price=60, max_guests=6
        )
        self.room_1 = Room.objects.create(
            name="Room 1.1",
            description="Room 1",
            room_type=self.room_type_simple,
        )
        self.room_2 = Room.objects.create(
            name="Room 2.1",
            description="Room 1",
            room_type=self.room_type_simple,
        )
        self.booking_1 = Booking.objects.create(
            state=Booking.NEW,
            checkin=datetime(2022, 12, 20).date(),
            checkout=datetime(2022, 12, 22).date(),
            guests=2,
            total=40,
            room=self.room_1,
        )
        self.booking_2 = Booking.objects.create(
            state=Booking.NEW,
            checkin=datetime(2022, 12, 23).date(),
            checkout=datetime(2022, 12, 25).date(),
            guests=2,
            total=40,
            room=self.room_1,
        )
        self.booking_3 = Booking.objects.create(
            state=Booking.NEW,
            checkin=datetime(2022, 12, 11).date(),
            checkout=datetime(2022, 12, 15).date(),
            guests=2,
            total=50,
            room=self.room_2,
        )
        self.url = reverse("edit_dates_booking", kwargs={"pk": self.booking_1.pk})

    def test_validate_name_of_html(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'edit_dates_booking.html')

    def test_form_instance(self):
        response = self.client.post(self.url, {
            "checkout": datetime(2022, 12, 28).date(),
            "checkin": datetime(2022, 12, 30).date()
        })
        self.assertIsInstance(response.context['form'], BookingEditDatesForm)

    def test_date_checkout_invalid(self):
        response = self.client.post(self.url, {
            "checkout": datetime(2022, 12, 28).date(),
            "checkin": datetime(2022, 12, 30).date()
        })
        self.assertContains(response, "checkout invalid", 1)
       
    def test_range_date_invalid(self):
        response = self.client.post(self.url, {
            "checkout": datetime(2022, 12, 30).date(),
            "checkin": datetime(2022, 12, 24).date()
        })
        self.assertContains(response, "Booking already exists with date", 1)

    def test_valid_success(self):
        response = self.client.post(self.url, {
            "checkout": datetime(2022, 12, 30).date(),
            "checkin": datetime(2022, 12, 26).date()
        })
        self.assertEqual(response.status_code, 302)
        booking = Booking.objects.get(id=self.booking_1.id)
        self.assertEqual(booking.checkout, datetime(2022, 12, 30).date())
        self.assertEqual(booking.checkin, datetime(2022, 12, 26).date())