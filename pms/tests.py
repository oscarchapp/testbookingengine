from datetime import datetime, timedelta
from django.test import TestCase, Client

from .models import *


# Create your tests here.
class TestEditBookingDates(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client = Client(enforce_csrf_checks=True)
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
        self.test_booking = Booking.objects.create(
            checkin=datetime.today(),
            checkout=datetime.today()+timedelta(days=1),
            room=test_room,
            guests=1,
            customer=test_customer,
            total=40
        )

    def test_new_link_in_home_view(self) -> None:
        response = self.client.get("")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
        self.assertContains(response, "/edit/dates")
    
    def test_edit_dates_template(self) -> None:
        url = "/booking/{}/edit/dates".format(self.test_booking.id)
        print(url)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "edit_booking_dates.html")

    def test_edit_dates(self) -> None:
        url = "/booking/{}/edit/dates".format(self.test_booking.id)
        new_checkin = datetime.today()+timedelta(days=1)
        new_checkout = datetime.today().replace(month=12, day=31)
        data = {
            'dates-checkin': new_checkin,
            'dates-checkout': new_checkout
        }
        response = self.client.post(
            url,
            data=data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 302)

        self.assertEqual(self.test_booking.checkin, new_checkin)
        self.assertEqual(self.test_booking.checkout, new_checkout)

    