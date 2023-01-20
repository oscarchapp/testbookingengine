from django.contrib.auth.models import User
from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import datetime


# Create your tests here.
from django.test import Client, TestCase
from django.urls import reverse

from .models import Booking, Customer, Room, Room_type
from .views import RoomsSearchView


class RoomsSearchViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.force_login(
            user=User.objects.create_user(
                "test_user", "test@example.com", "test_password"
            )
        )
        self.room_type = Room_type.objects.create(
            name="Single", price=100, max_guests=1
        )
        self.room_type2 = Room_type.objects.create(
            name="Double", price=200, max_guests=2
        )
        self.room = Room.objects.create(
            room_type=self.room_type, name="Single 1", description="Single room"
        )
        self.room2 = Room.objects.create(
            room_type=self.room_type2, name="Double 2", description="Double room"
        )
        self.customer = Customer.objects.create(
            name="John Doe", email="test@test.me", phone="123456789"
        )
        self.booking = Booking.objects.create(
            checkin=datetime.datetime.now().date(),
            checkout=(datetime.datetime.now() + datetime.timedelta(days=10)).date(),
            room=self.room,
            guests=1,
            total=100,
            code="12345678",
            customer=self.customer,
            state=Booking.NEW,
        )
        self.booking2 = Booking.objects.create(
            checkin=(datetime.datetime.now() + datetime.timedelta(days=30)).date(),
            checkout=(datetime.datetime.now() + datetime.timedelta(days=40)).date(),
            room=self.room2,
            guests=2,
            total=200,
            code="12345679",
            customer=self.customer,
            state=Booking.NEW,
        )

    def test_get_rooms_search_matching(self):
        endpoint = reverse("rooms_search")
        response = self.client.get(endpoint, {"filter": "sin"})
        self.assertEqual(response.status_code, 200)
        # There is one room with sin in the name
        self.assertEqual(
            response.context["rooms"].count(), 1, response.context["rooms"].count()
        )

    def test_get_rooms_search_not_matching(self):
        endpoint = reverse("rooms_search")
        response = self.client.get(endpoint, {"filter": "triple"})
        self.assertEqual(response.status_code, 200)
        # There aren't any rooms with triple in the name
        self.assertEqual(
            response.context["rooms"].count(), 0, response.context["rooms"].count()
        )

    def test_get_dashboard_percentage_of_occupation(self):
        endpoint = reverse("dashboard")
        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, 200)
        # There are 2 rooms and only one has booking (today) so the percentage of occupation should be 50%
        self.assertEqual(
            response.context["dashboard"]["occupation"],
            50,
            response.context["dashboard"]["occupation"],
        )

    def test_edit_booking_fail(self):
        endpoint = reverse("booking_edit", kwargs={"pk": self.booking2.pk})
        response = self.client.post(
            endpoint,
            data={
                "booking-checkin": (
                    datetime.datetime.now() + datetime.timedelta(days=50)
                ).date(),
                "booking-checkout": (
                    datetime.datetime.now() + datetime.timedelta(days=10)
                ).date(),
            },
        )

        booking = Booking.objects.get(pk=self.booking2.pk)
        self.assertNotEqual(booking.checkin, datetime.datetime.now().date())

    def test_edit_booking_success(self):
        endpoint = reverse("booking_edit", kwargs={"pk": self.booking2.pk})
        response = self.client.post(
            endpoint,
            data={
                "booking-checkin": (
                    datetime.datetime.now() + datetime.timedelta(days=30)
                ).date(),
                "booking-checkout": (
                    datetime.datetime.now() + datetime.timedelta(days=50)
                ).date(),
            },
        )
        booking = Booking.objects.get(pk=self.booking2.pk)
        self.assertEqual(
            booking.checkin,
            (datetime.datetime.now() + datetime.timedelta(days=30)).date(),
        )
