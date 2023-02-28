from datetime import date, timedelta
from django.core.exceptions import ValidationError
from django.test import TestCase
from pms.models import Booking, Room, Room_type, Customer


class BookingCreationTest(TestCase):
    def setUp(self):
        room_type = Room_type.objects.create(name="multiple", price=50, max_guests=5)
        room = Room.objects.create(room_type=room_type, name="Room 1.1", description="The Room")
        customer = Customer.objects.create(name='Marco', email='marco@prueba.com', phone="600123456")

    def test_booking_creation(self):
        """Tests a booking can be successfully crreated with the correct data."""
        booking_data = {
            "state": Booking.NEW,
            "checkin": date(2022, 1, 1),
            "checkout": date(2022, 1, 2),
            "room": Room.objects.first(),
            "guests": 3,
            "customer": Customer.objects.first(),
            "code": "00000000",
        }

        booking = Booking.objects.create(**booking_data)
        self.assertEqual(Booking, type(booking))

    def test_booking_creation_when_checkin_date_equals_MAX_ALLOWED_DATE(self):
        """ Check ValidationError raising when chekin date is equal to Booking.MAX_ALLOWED_DATE."""
        booking_data = {
            "state": Booking.NEW,
            "checkin": Booking.MAX_ALLOWED_DATE,
            "checkout": Booking.MAX_ALLOWED_DATE,
            "room": Room.objects.first(),
            "guests": 3,
            "customer": Customer.objects.first(),
            "code": "00000002",
        }
        booking = Booking.objects.create(**booking_data)
        self.assertEqual(Booking, type(booking))

    def test_booking_creation_when_checkout_date_equals_MAX_ALLOWED_DATE(self):
        """ Check ValidationError raising when chekout date is equal to Booking.MAX_ALLOWED_DATE."""
        booking_data = {
            "state": Booking.NEW,
            "checkin": date(2022, 1, 1),
            "checkout": Booking.MAX_ALLOWED_DATE,
            "room": Room.objects.first(),
            "guests": 3,
            "customer": Customer.objects.first(),
            "code": "00000003",
        }
        booking = Booking.objects.create(**booking_data)
        self.assertEqual(Booking, type(booking))

    def test_booking_creation_raises_validationerror_when_checkin_date_overcomes_MAX_ALLOWED_DATE(self):
        """ Check ValidationError raising when checkin date is newer than Booking.MAX_ALLOWED_DATE."""
        booking_data = {
            "state": Booking.NEW,
            "checkin": Booking.MAX_ALLOWED_DATE + timedelta(days=1),
            "checkout": Booking.MAX_ALLOWED_DATE + timedelta(days=1),
            "room": Room.objects.first(),
            "guests": 3,
            "customer": Customer.objects.first(),
            "code": "00000004",
        }
        self.assertRaises(ValidationError, Booking.objects.create, **booking_data)

    def test_booking_creation_raises_validationerror_when_checkout_date_overcomes_MAX_ALLOWED_DATE(self):
        """ Check ValidationError raising when chekout date is newer than Booking.MAX_ALLOWED_DATE."""
        booking_data = {
            "state": Booking.NEW,
            "checkin": date(2022, 1, 1),
            "checkout": Booking.MAX_ALLOWED_DATE + timedelta(days=1),
            "room": Room.objects.first(),
            "guests": 3,
            "customer": Customer.objects.first(),
            "code": "00000005",
        }
        self.assertRaises(ValidationError, Booking.objects.create, **booking_data)

    def test_booking_creation_raises_validationerror_when_checkin_date_is_newer_than_checkout_date(self):
        """
        Check ValidationError raising when checkin date is newer than checkout date.
        Requirements:
            - Both dates must be older or equal than Booking.MAX_ALLOWED_DATE.
        """
        booking_data = {
            "state": Booking.NEW,
            "checkin": date(2022, 1, 2),
            "checkout": date(2022, 1, 1),
            "room": Room.objects.first(),
            "guests": 3,
            "customer": Customer.objects.first(),
            "code": "00000006",
        }
        self.assertRaises(ValidationError, Booking.objects.create, **booking_data)

    def test_booking_creation_calculates_correct_price(self):
        """ Check correct price calculation when a booking is created."""
        room = Room.objects.first()
        start_date = date(2022, 5, 1)
        end_date = date(2022, 5, 2)
        booking_data = {
            "state": Booking.NEW,
            "checkin": start_date,
            "checkout": end_date,
            "room": room,
            "guests": 3,
            "customer": Customer.objects.first(),
            "code": "00000007",
        }
        EXECTED_PRICE = Booking._booking_days(start_date, end_date) * room.room_type.price
        booking = Booking.objects.create(**booking_data)
        self.assertEqual(booking.total, EXECTED_PRICE)


class BookingUpdateTest(TestCase):
    def setUp(self):
        room_type = Room_type.objects.create(name="multiple", price=50, max_guests=5)
        room = Room.objects.create(room_type=room_type, name="Room 1.1", description="The Room")
        customer = Customer.objects.create(name='Marco', email='marco@prueba.com', phone="600123456")
        booking_data = {
            "state": Booking.NEW,
            "checkin": date(2022, 1, 1),
            "checkout": date(2022, 2, 2),
            "room": room,
            "guests": 3,
            "customer": customer,
            "code": "00000000",
        }
        booking = Booking.objects.create(**booking_data)

    def test_booking_update_when_dates_are_correct(self):
        """Tests a booking can be successfully updated with the correct data."""
        booking = Booking.objects.first()
        start_date = date(2022, 1, 1)
        end_date = date(2022, 1, 2)
        booking.checkin = start_date
        booking.checkout = end_date
        booking.save()
        self.assertEqual(start_date, booking.checkin)
        self.assertEqual(end_date, booking.checkout)

    def test_booking_update_when_checkin_date_equals_MAX_ALLOWED_DATE(self):
        """ Check update when chekin date is equal to Booking.MAX_ALLOWED_DATE."""
        booking = Booking.objects.first()
        start_date = Booking.MAX_ALLOWED_DATE
        end_date = Booking.MAX_ALLOWED_DATE
        booking.checkin = start_date
        booking.checkout = end_date
        booking.save()
        self.assertEqual(start_date, booking.checkin)
        self.assertEqual(end_date, booking.checkout)

    def test_booking_update_when_checkout_date_equals_MAX_ALLOWED_DATE(self):
        """ Check update when chekout date is equal to Booking.MAX_ALLOWED_DATE."""
        booking = Booking.objects.first()
        start_date = Booking.MAX_ALLOWED_DATE + timedelta(days=-1)
        end_date = Booking.MAX_ALLOWED_DATE
        booking.checkin = start_date
        booking.checkout = end_date
        booking.save()
        self.assertEqual(start_date, booking.checkin)
        self.assertEqual(end_date, booking.checkout)

    def test_booking_update_raises_validationerror_when_checkin_date_overcomes_MAX_ALLOWED_DATE(self):
        """ Check ValidationError raising when checkin date is newer than Booking.MAX_ALLOWED_DATE."""
        booking = Booking.objects.first()
        booking.checkin = Booking.MAX_ALLOWED_DATE + timedelta(days=1)
        booking.checkout = Booking.MAX_ALLOWED_DATE + timedelta(days=1)
        self.assertRaises(ValidationError, booking.save)

    def test_booking_update_raises_validationerror_when_checkout_date_overcomes_MAX_ALLOWED_DATE(self):
        """ Check ValidationError raising when chekout date is newer than Booking.MAX_ALLOWED_DATE."""
        booking = Booking.objects.first()
        booking.checkin = date(2022, 1, 1)
        booking.checkout = Booking.MAX_ALLOWED_DATE + timedelta(days=1)
        self.assertRaises(ValidationError, booking.save)

    def test_booking_update_raises_validationerror_when_checkin_date_is_newer_than_checkout_date(self):
        """
        Check ValidationError raising when checkin date is newer than checkout date.
        Requirements:
            - Both dates must be older or equal than Booking.MAX_ALLOWED_DATE.
        """
        booking = Booking.objects.first()
        booking.checkin = date(2022, 1, 2)
        booking.checkout = date(2023, 1, 1)
        self.assertRaises(ValidationError, booking.save)

    def test_booking_update_calculates_correct_price(self):
        """ Check correct price calculation when a booking is created."""
        booking = Booking.objects.first()
        room = booking.room
        start_date = date(2022, 5, 1)
        end_date = date(2022, 5, 5)
        EXECTED_PRICE = Booking._booking_days(start_date, end_date) * room.room_type.price
        booking.checkin = start_date
        booking.checkout = end_date
        booking.save()
        self.assertEqual(booking.total, EXECTED_PRICE)


class BookingManagerObjects(TestCase):

    DEFAULT_START_DATE = date(2022, 2, 1)
    DEFAULT_END_DATE = date(2022, 2, 15)
    DEFAULT_CLASH_START_DATE = date(2022, 2, 25)
    DEFAULT_CLASH_END_DATE = date(2022, 3, 3)

    def setUp(self):
        room_type = Room_type.objects.create(name="multiple", price=50, max_guests=5)
        customer = Customer.objects.create(name='Marco', email='marco@prueba.com', phone="600123456")
        room = Room.objects.create(room_type=room_type, name="Room 1.1", description="The Room")

        # Booking 1 // room1
        booking_data = {
            "state": Booking.NEW,
            "checkin": self.DEFAULT_START_DATE,
            "checkout": self.DEFAULT_END_DATE,
            "room": room,
            "guests": 3,
            "customer": customer,
            "code": "00000000",
        }
        booking = Booking.objects.create(**booking_data)
        self.booking = booking

        # Booking 2 // room_2
        booking_data_2 = {
            "state": Booking.NEW,
            "checkin": self.DEFAULT_CLASH_START_DATE,
            "checkout": self.DEFAULT_CLASH_END_DATE,
            "room": room,
            "guests": 3,
            "customer": customer,
            "code": "00000001",
        }
        booking_2 = Booking.objects.create(**booking_data_2)
        self.booking_2 = booking_2

    ###  OUR BOOKING
    def test_booking_room_is_available_when_new_daterange_clashes_with_actual_date_but_is_our_booking(self):
        """
        Check room is available when new date range is a subset of actual booking date range, but who's updating
        the dates is the manager of the same booking.
        When me manage our own booking whe must be available to change dates even if new date range clashes with
        the old one in order to allow extension/reduction of our booking.
        Requirements:
            - The booking with conflictive dates must be the same the booking to be compared by `is_room_available`
              function.
        """
        booking = Booking.objects.first()
        start_date = self.DEFAULT_START_DATE
        end_date = self.DEFAULT_END_DATE
        is_available = Booking.objects.is_room_available(booking, from_date=start_date, to_date=end_date)
        self.assertEqual(is_available, True)

    def test_booking_room_is_available_when_new_daterange_does_not_clash_with_our_booking_dates_from_right(self):
        """
        Check room is available when new date range is completely different and newer from our actual booking
        date range and does not clashes with actual nor other bookings date ranges for this room.
        Requirements:
            - New date range cannot intersect with actual booking date range.
            - New date range checkin date must be newer than actual date range checkout.
            - New date range cannot clash with another booking over this room.
        """
        booking = self.booking
        start_date = self.DEFAULT_END_DATE + timedelta(days=1)
        end_date = self.DEFAULT_END_DATE + timedelta(days=2)
        is_available = Booking.objects.is_room_available(booking, from_date=start_date, to_date=end_date)
        self.assertEqual(is_available, True)

    def test_booking_room_is_available_when_new_daterange_almost_does_not_clash_with_our_booking_dates_from_right(self):
        """
        The same as test_booking_room_is_available_when_new_date_does_not_clash_with_our_booking_dates_from_right
        but this time new date range checkin clashes with actual date range checkout.
        """
        booking = self.booking
        start_date = self.DEFAULT_END_DATE
        end_date = self.DEFAULT_END_DATE + timedelta(days=2)
        is_available = Booking.objects.is_room_available(booking, from_date=start_date, to_date=end_date)
        self.assertEqual(is_available, True)

    def test_booking_room_is_available_when_new_daterange_intersects_with_our_booking_dates_from_right(self):
        """
        The same as test_booking_room_is_available_when_new_daterange_does_not_clash_with_our_booking_dates_from_right
        but this time new date range checkin is newer than than actual date range checkout and new date range checkout
        is older than actual date range checkout.
        """
        booking = self.booking
        start_date = self.DEFAULT_END_DATE + timedelta(days=-5)
        end_date = self.DEFAULT_END_DATE + timedelta(days=5)
        is_available = Booking.objects.is_room_available(booking, from_date=start_date, to_date=end_date)
        self.assertEqual(is_available, True)

    def test_booking_room_is_available_when_new_daterange_does_not_clash_with_our_booking_dates_from_left(self):
        """
        Check room is available when new date range is completely different and older from our actual booking
        date range and does not clashes with actual nor other bookings date ranges for this room.
        Requirements:
            - New date range cannot intersect with actual booking date range.
            - New date range chekout date must be older than actual date range checkin.
            - New date range cannot clash with another booking over this room.
        """
        booking = self.booking
        start_date = self.DEFAULT_START_DATE + timedelta(days=-5)
        end_date = self.DEFAULT_START_DATE + timedelta(days=-1)
        is_available = Booking.objects.is_room_available(booking, from_date=start_date, to_date=end_date)
        self.assertEqual(is_available, True)

    def test_booking_room_is_available_when_new_daterange_almost_does_not_clash_with_our_booking_dates_from_left(self):
        """
        The same as test_booking_room_is_available_when_new_date_does_not_clash_with_our_booking_dates_from_left
        but this time new date range checkout clashes with actual date range checkin.
        """
        booking = self.booking
        start_date = self.DEFAULT_START_DATE + timedelta(days=-5)
        end_date = self.DEFAULT_START_DATE
        is_available = Booking.objects.is_room_available(booking, from_date=start_date, to_date=end_date)
        self.assertEqual(is_available, True)

    def test_booking_room_is_available_when_new_daterange_intersects_with_our_booking_dates_from_left(self):
        """
        The same as test_booking_room_is_available_when_new_daterange_does_not_clash_with_our_booking_dates_from_left
        but this time new date range checkin is older than than actual date range checkout and new date range checkout
        is newer than actual date range checkout.
        """
        booking = self.booking
        start_date = self.DEFAULT_START_DATE + timedelta(days=-5)
        end_date = self.DEFAULT_START_DATE + timedelta(days=5)
        is_available = Booking.objects.is_room_available(booking, from_date=start_date, to_date=end_date)
        self.assertEqual(is_available, True)


    ###  POSSIBLE CONFLICTS WIRH ANOTHER BOOKING OVER THE SAME ROOM
    def test_booking_room_is_NOT_available_when_new_daterange_almost_clashes_with_another_booking_dates_from_right(self):
        """
        Check room is not available when new date range checkin clashes with another booking checkout over the same room.
        """
        booking = self.booking
        start_date = self.DEFAULT_CLASH_END_DATE
        end_date = self.DEFAULT_CLASH_END_DATE + timedelta(days=2)
        is_available = Booking.objects.is_room_available(booking, from_date=start_date, to_date=end_date)
        self.assertEqual(is_available, False)

    def test_booking_room_is_NOT_available_when_new_daterange_intersects_with_another_booking_dates_from_right(self):
        """
        The same as test_booking_room_is_NOT_available_when_new_daterange_almost_clashes_with_another_booking_dates_from_right
        but this time new date range checkin is newer than than actual date range checkout and new date range checkout
        is older than actual date range checkout.
        """
        booking = self.booking
        start_date = self.DEFAULT_CLASH_END_DATE + timedelta(days=-2)
        end_date = self.DEFAULT_CLASH_END_DATE + timedelta(days=2)
        is_available = Booking.objects.is_room_available(booking, from_date=start_date, to_date=end_date)
        self.assertEqual(is_available, False)

    def test_booking_room_is_NOT_available_when_new_daterange_almost_clashes_with_another_booking_dates_from_left(self):
        """
        Check room is not available when new date range checkout clashes with another booking checkin over the same room.
        """
        booking = self.booking
        start_date = self.DEFAULT_CLASH_START_DATE + timedelta(days=-2)
        end_date = self.DEFAULT_CLASH_START_DATE
        is_available = Booking.objects.is_room_available(booking, from_date=start_date, to_date=end_date)
        self.assertEqual(is_available, False)

    def test_booking_room_is_NOT_available_when_new_daterange_intersects_with_another_booking_dates_from_left(self):
        """
        The same as test_booking_room_is_NOT_available_when_new_daterange_almost_clashes_with_another_booking_dates_from_left
        but this time new date range checkout is newer than than actual date range checkin and new date range checkin
        is older than actual date range checkin.
        """
        booking = self.booking
        start_date = self.DEFAULT_CLASH_START_DATE + timedelta(days=-2)
        end_date = self.DEFAULT_CLASH_START_DATE + timedelta(days=2)
        is_available = Booking.objects.is_room_available(booking, from_date=start_date, to_date=end_date)
        self.assertEqual(is_available, False)




    
