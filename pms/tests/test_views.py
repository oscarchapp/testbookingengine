from django.test import TestCase
from django.urls import reverse
from datetime import datetime, timedelta
from pms.models import Booking, Room, Room_type

# Create your tests here.
class DashboardViewTest(TestCase):
    def setUp(self):
        self.url = reverse("dashboard")
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
        self.room_3 = Room.objects.create(
            name="Room 3.1",
            description="Room 1",
            room_type=self.room_type_simple,
        )
        self.room_3_2 = Room.objects.create(
            name="Room 3.2",
            description="Room 1",
            room_type=self.room_type_simple,
        )
        self.room_4 = Room.objects.create(
            name="Room 4.1",
            description="Room 1",
            room_type=self.room_type_simple,
        )
        self.room_4_2 = Room.objects.create(
            name="Room 4.2",
            description="Room 1",
            room_type=self.room_type_simple,
        )
        self.today = datetime.today()
        self.tomorrow = self.today + timedelta(days=1)
        self.yesterday = self.today - timedelta(days=1)
        # bookings waiting
        self.booking_1 = Booking.objects.create(
            state=Booking.NEW,
            checkin=self.yesterday,
            checkout=self.tomorrow,
            guests=2,
            total=40,
            room=self.room_1,
        )
        self.booking_2 = Booking.objects.create(
            state=Booking.NEW,
            checkin=self.yesterday,
            checkout=self.tomorrow,
            guests=2,
            total=50,
            room=self.room_2,
        )
        self.booking_3 = Booking.objects.create(
            state=Booking.NEW,
            checkin=self.yesterday,
            checkout=self.tomorrow,
            guests=2,
            total=60,
            room=self.room_3,
        )
        # occupied bookings
        self.booking_4 = Booking.objects.create(
            state=Booking.NEW,
            checkin=self.yesterday,
            checkout=self.today,
            guests=2,
            total=40,
            room=self.room_1,
        )
        self.booking_5 = Booking.objects.create(
            state=Booking.DELETED,
            checkin=self.yesterday,
            checkout=self.tomorrow,
            guests=2,
            total=40,
            room=self.room_1,
        )

    def test_percentage_value_50(self):

        response = self.client.get(self.url)
        context = response.context
        self.assertEqual(context["dashboard"]["percentage_by_occupation"], 50)

    def test_percentage_value_100(self):
        self.booking_6 = Booking.objects.create(
            state=Booking.NEW,
            checkin=self.yesterday,
            checkout=self.tomorrow,
            guests=2,
            total=40,
            room=self.room_4,
        )
        self.booking_7 = Booking.objects.create(
            state=Booking.NEW,
            checkin=self.yesterday,
            checkout=self.tomorrow,
            guests=2,
            total=40,
            room=self.room_4_2,
        )
        self.booking_8 = Booking.objects.create(
            state=Booking.NEW,
            checkin=self.yesterday,
            checkout=self.tomorrow,
            guests=2,
            total=40,
            room=self.room_3_2,
        )
        response = self.client.get(self.url)
        context = response.context
        self.assertEqual(context["dashboard"]["percentage_by_occupation"], 100)
