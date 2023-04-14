from datetime import date, timedelta

from django.test import TestCase
from django.urls import reverse, resolve

from pms.models import Room_type, Room, Booking, Customer
from pms.views import EditBookingDatesView


class EditBookingDatesViewTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):

        # Create customers
        cls.customer_1 = Customer.objects.create(name="customer 1", email="customer_1@test.com", phone="123456789")
        cls.customer_2 = Customer.objects.create(name="customer 2", email="customer_1@test.com", phone="123456789")

        # Create rooms
        room_type_simple = Room_type.objects.create(name="Simple", price=20, max_guests=1)
        room_type_double = Room_type.objects.create(name="Double", price=40, max_guests=2)

        cls.room_simple = Room.objects.create(room_type=room_type_simple, name="Room Simple", description="description simple")

        # Make random date check in and checkout
        cls.check_in = date(2020, 4, 15)
        cls.check_out = date(2020, 4, 17)

        # Create bookings
        cls.booking_room_simple_1 = Booking.objects.create(
            checkin=cls.check_in,
            checkout=cls.check_out,
            room=cls.room_simple,
            guests=1,
            customer=cls.customer_1,
            total=40,
            code="1234"
        )

        cls.booking_room_simple_2 = Booking.objects.create(
            checkin=date(2020, 4, 20),
            checkout=date(2020, 4, 25),
            room=cls.room_simple,
            guests=1,
            customer=cls.customer_2,
            total=20,
            code="1234"
        )

        cls.url = reverse("edit_booking_dates", kwargs={"pk": cls.booking_room_simple_1.pk})
        cls.body = {
            "checkin": date(2020, 4, 15),
            "checkout": date(2020, 4, 18)
        }

        return super().setUpTestData()

    def test_GET_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_POST_status_code(self):
        response = self.client.post(self.url, self.body)
        self.assertEqual(response.status_code, 302)

    def test_url_resolves(self):
        view_class = resolve(self.url).func.view_class
        self.assertEqual(view_class, EditBookingDatesView)

    def test_GET_template_name(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "edit_booking_dates.html")

    def test_POST_redirect(self):
        response = self.client.post(self.url, self.body)
        self.assertEqual(reverse("home"), response.url)

    def test_GET_context_data(self):
        response = self.client.get(self.url)
        context = response.context
        self.assertIn("url_home", context)
        self.assertEqual(reverse("home"), context["url_home"])

    def test_edit_booking_dates_not_available_check_out(self):
        body = self.body.copy()
        body["checkout"] = self.booking_room_simple_2.checkout - timedelta(days=1)
        response = self.client.post(self.url, body)

        self.assertFalse(response.context_data["form"].is_valid())

        body["checkout"] = self.booking_room_simple_2.checkout
        response = self.client.post(self.url, body)

        self.assertFalse(response.context_data["form"].is_valid())

        body["checkout"] = self.booking_room_simple_2.checkout + timedelta(days=1)
        response = self.client.post(self.url, body)

        self.assertFalse(response.context_data["form"].is_valid())

    def test_edit_booking_dates_not_available_check_in(self):
        body = self.body.copy()
        body["checkin"] = self.booking_room_simple_2.checkin - timedelta(days=1)
        body["checkout"] = self.booking_room_simple_2.checkout + timedelta(days=1)
        response = self.client.post(self.url, body)

        self.assertFalse(response.context_data["form"].is_valid())

        body["checkin"] = self.booking_room_simple_2.checkin
        response = self.client.post(self.url, body)

        self.assertFalse(response.context_data["form"].is_valid())

        body["checkin"] = self.booking_room_simple_2.checkin + timedelta(days=1)
        response = self.client.post(self.url, body)

        self.assertFalse(response.context_data["form"].is_valid())

    def test_edit_booking_dates_available_date(self):
        body = self.body.copy()
        body["checkin"] = self.booking_room_simple_2.checkin - timedelta(days=1)
        body["checkout"] = self.booking_room_simple_2.checkin
        response = self.client.post(self.url, body)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(reverse("home"), response.url)

        body["checkin"] = self.booking_room_simple_2.checkout
        body["checkout"] = self.booking_room_simple_2.checkout + timedelta(days=1)
        response = self.client.post(self.url, body)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(reverse("home"), response.url)

    def test_edit_booking_dates_reverse_dates(self):
        body = self.body.copy()
        body["checkin"] = self.body["checkout"]
        body["checkout"] = self.body["checkin"]
        response = self.client.post(self.url, body)

        self.assertFalse(response.context_data["form"].is_valid())

