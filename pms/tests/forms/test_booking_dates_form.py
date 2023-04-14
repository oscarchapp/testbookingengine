from datetime import date, timedelta

from django.test import TestCase

from pms.forms import BookingDatesForm
from pms.models import Room_type, Room, Booking, Customer


class BookingDatesFormTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.form = BookingDatesForm

        # Create customers
        cls.customer_1 = Customer.objects.create(name="customer 1", email="customer_1@test.com", phone="123456789")
        cls.customer_2 = Customer.objects.create(name="customer 2", email="customer_1@test.com", phone="123456789")

        # Create rooms
        room_type_simple = Room_type.objects.create(name="Simple", price=20, max_guests=1)

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

        return super().setUpTestData()

    def test_booking_dates_form_valid(self):
        form_data = {
            'checkin': self.check_in - timedelta(days=1),
            'checkout': self.check_out
        }
        form = BookingDatesForm(data=form_data, instance=self.booking_room_simple_1)
        self.assertTrue(form.is_valid())

    def test_booking_dates_form_same_dates(self):
        form_data = {
            'checkin': self.check_in,
            'checkout': self.check_in
        }
        form = BookingDatesForm(data=form_data, instance=self.booking_room_simple_1)
        self.assertFalse(form.is_valid())

    def test_booking_dates_form_reverse_dates(self):
        form_data = {
            'checkin': self.check_out,
            'checkout': self.check_in
        }
        form = BookingDatesForm(data=form_data, instance=self.booking_room_simple_1)
        self.assertFalse(form.is_valid())

    def test_booking_dates_form_overlapping_dates_checkout(self):
        form_data = {
            'checkin': self.check_in,
            'checkout': self.booking_room_simple_2.checkout
        }
        form = BookingDatesForm(data=form_data, instance=self.booking_room_simple_1)
        self.assertFalse(form.is_valid())

        form_data['checkout'] = self.booking_room_simple_2.checkout + timedelta(days=1)
        form = BookingDatesForm(data=form_data, instance=self.booking_room_simple_1)
        self.assertFalse(form.is_valid())

        form_data['checkout'] = self.booking_room_simple_2.checkout - timedelta(days=1)
        form = BookingDatesForm(data=form_data, instance=self.booking_room_simple_1)
        self.assertFalse(form.is_valid())

    def test_booking_dates_form_overlapping_dates_checkin(self):
        form_data = {
            'checkin': self.booking_room_simple_2.checkin,
            'checkout': self.booking_room_simple_2.checkout
        }
        form = BookingDatesForm(data=form_data, instance=self.booking_room_simple_1)
        self.assertFalse(form.is_valid())

        form_data['checkin'] = self.booking_room_simple_2.checkin - timedelta(days=1)
        form = BookingDatesForm(data=form_data, instance=self.booking_room_simple_1)
        self.assertFalse(form.is_valid())

        form_data['checkin'] = self.booking_room_simple_2.checkin + timedelta(days=1)
        form = BookingDatesForm(data=form_data, instance=self.booking_room_simple_1)
        self.assertFalse(form.is_valid())

    def test_booking_dates_form_overlapping_dates(self):
        form_data = {
            'checkin': self.booking_room_simple_2.checkin - timedelta(days=1),
            'checkout': self.booking_room_simple_2.checkout + timedelta(days=1)
        }
        form = BookingDatesForm(data=form_data, instance=self.booking_room_simple_1)
        self.assertFalse(form.is_valid())

    def test_booking_dates_form_save(self):
        form_data = {
            'checkin': self.check_in - timedelta(days=1),
            'checkout': self.check_out
        }
        days_booked = (form_data["checkout"] - form_data["checkin"]).days
        form = BookingDatesForm(data=form_data, instance=self.booking_room_simple_1)
        form.is_valid()
        form.save()
        self.booking_room_simple_1.refresh_from_db()

        total_payed = days_booked * self.booking_room_simple_1.room.room_type.price
        self.assertEqual(self.booking_room_simple_1.total, total_payed)
