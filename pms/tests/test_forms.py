from django.test import TestCase
from pms.models import Room, Room_type, Booking
from pms.forms import BookingEditDatesForm
from datetime import datetime, timedelta

class BookingEditDatesFormTest(TestCase):

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
    
    def test_date_checkout_invalid(self):
        booking_form = BookingEditDatesForm({
            "checkout": datetime(2022, 12, 28).date(),
            "checkin": datetime(2022, 12, 30).date()
        }, instance=self.booking_1)
        self.assertFalse(booking_form.is_valid())
        self.assertEqual(booking_form.errors["checkout"], ["checkout invalid"])

    def test_date_checkin_invalid(self):
        today = datetime.today().date()
        yesterday = today - timedelta(days=1)
        booking_form = BookingEditDatesForm({
            "checkout": datetime(2022, 12, 30).date(),
            "checkin": yesterday
        }, instance=self.booking_1)
        self.assertFalse(booking_form.is_valid())
        self.assertEqual(booking_form.errors["checkin"], ["checkin invalid"])

    def test_range_date_invalid(self):
        booking_form = BookingEditDatesForm({
            "checkout": datetime(2022, 12, 30).date(),
            "checkin": datetime(2022, 12, 24).date()
        }, instance=self.booking_1)
        self.assertFalse(booking_form.is_valid())
        self.assertEqual(booking_form.errors["__all__"], ["Booking already exists with date"])

    def test_valid_success(self):
        today = datetime.today().date()
        more_days = today + timedelta(days=3)
        booking_form = BookingEditDatesForm({
            "checkout": more_days,
            "checkin": today
        }, instance=self.booking_1)
        self.assertTrue(booking_form.is_valid())
