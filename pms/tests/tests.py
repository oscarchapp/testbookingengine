from django.test import TestCase
from datetime import date, timedelta
from pms.models import Room, Booking
from pms.tests.factory import BookingFactory, RoomFactory
from pms.tests.data import PERCENT_TEST

ROOM_NAMES = ["R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "R10"]


class RoomPercentOcuppationTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        for room_name in ROOM_NAMES:
            RoomFactory.create(name=room_name)

    def test_percent_occupation(self):
        """
        Test room occupancy percentage
        Warning: Future reservations are ignored
        """
        today = date.today()
        for b in PERCENT_TEST:
            BookingFactory.create(
                room=Room.objects.get(name=b["room"]),
                state=b["state"],
                checkin=today + timedelta(days=b["checkin"]),
                checkout=today + timedelta(days=b["checkout"])
            )
            self.assertEqual(Room.get_percent_occupation(), b["percent"])


class DashboardDataWidgetTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        for room_name in ROOM_NAMES:
            RoomFactory.create(name=room_name)

        today = date.today()
        for b in PERCENT_TEST:
            booking = BookingFactory.create(
                room=Room.objects.get(name=b["room"]),
                state=b["state"],
                checkin=today + timedelta(days=b["checkin"]),
                checkout=today + timedelta(days=b["checkout"]),
                total = b["total"]
            )
            booking.created = today + timedelta(days=b["created"])
            booking.save()

    def test_new_bookings(self):
        """
        Test all bookings that were created today.
        """
        new_bookings = len([d for d in PERCENT_TEST if d["created"] == 0])
        self.assertEqual(Booking.get_news(count_only=True), new_bookings)

    def test_incoming(self):
        """
        Test all bookings confirmed and whose checkin date is today
        """
        incoming = len([
            d for d in PERCENT_TEST
            if d["checkin"] == 0 and d["state"] == Booking.NEW
        ])
        self.assertEqual(Booking.get_incoming(count_only=True), incoming)

    def test_outcoming(self):
        """
        Test all bookings confirmed and whose checkout date is today
        """
        outcoming = len([
            d for d in PERCENT_TEST
            if d["checkout"] == 0 and d["state"] == Booking.NEW
        ])
        self.assertEqual(Booking.get_outcoming(count_only=True), outcoming)

    def test_invoiced(self):
        """
        Test calculate invoices for all confirmed bookings that were created today
        """
        invoiced = sum([
            d["total"] for d in PERCENT_TEST
            if d["created"] == 0 and d["state"] == Booking.NEW
        ])
        self.assertEqual(Booking.get_invoiced().get("total__sum"), invoiced)
