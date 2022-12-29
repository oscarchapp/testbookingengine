from datetime import datetime, timedelta
from django.test import TestCase, Client
from django.middleware.csrf import CsrfViewMiddleware
from unittest.mock import patch

from .models import *
from .form_dates.dates_limits import get_checkout_min_date, get_checkout_max_date


class TestEditBookingDates(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client = Client()
        test_room_type = Room_type.objects.create(
            name="individual",
            price=40,
            max_guests=1
        )
        test_room = Room.objects.create(
            room_type=test_room_type,
            name="Room 1.1",
            description="Test room"
        )
        test_customer = Customer.objects.create(
            name="Test customer",
            email="test_customer@gmail.com",
            phone="666666666"
        )
        test_booking = Booking.objects.create(
            checkin=datetime.today(),
            checkout=datetime.today()+timedelta(days=1),
            room=test_room,
            guests=1,
            customer=test_customer,
            total=40
        )
        self.test_booking_id = test_booking.id

    def test_new_link_in_home_view(self) -> None:
        response = self.client.get("")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
        self.assertContains(response, "/edit/dates")
    
    def test_edit_dates_template(self) -> None:
        url = "/booking/{}/edit/dates".format(self.test_booking_id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "edit_booking_dates.html")

    @patch.object(CsrfViewMiddleware, "_set_csrf_cookie")
    def test_edit_dates(self, mock_csrf) -> None:
        url = "/booking/{}/edit/dates".format(self.test_booking_id)
        new_checkin = datetime.today()+timedelta(days=1)
        new_checkout = datetime.today().replace(month=12, day=31)
        data = 'dates-checkin={}&dates-checkout={}'.format(
            new_checkin.strftime("%Y-%m-%d"),
            new_checkout.strftime("%Y-%m-%d")
        )
        response = self.client.post(
            url,
            data,
            content_type="application/x-www-form-urlencoded"
        )
        self.assertEqual(response.status_code, 302)

        updated_booking = Booking.objects.get(id=self.test_booking_id)
        self.assert_dates_equal(updated_booking.checkin, new_checkin)
        self.assert_dates_equal(updated_booking.checkout, new_checkout)

    def assert_dates_equal(self, date, expected_date):
        """
        Compares two dates and checks if year, month and day have the same values
        """
        day = date.day
        expected_day = expected_date.day
        month = date.month
        expected_month = expected_date.month
        year = date.year
        expected_year = expected_date.year

        return (
            self.assertEqual(day, expected_day)
            and self.assertEqual(month, expected_month)
            and self.assertEqual(year, expected_year)
        )
