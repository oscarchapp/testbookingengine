from datetime import date, time, datetime
from unittest.mock import patch

from django.db.models import Sum, Q
from django.test import TestCase
from django.urls import reverse, resolve

from pms.models import Room_type, Room, Booking, Customer
from pms.views import DashboardView


class DashboardViewTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("dashboard")

        # Create customers
        cls.customer_1 = Customer.objects.create(name="customer 1", email="customer_1@test.com", phone="123456789")
        cls.customer_2 = Customer.objects.create(name="customer 2", email="customer_1@test.com", phone="123456789")
        cls.customer_3 = Customer.objects.create(name="customer 3", email="customer_1@test.com", phone="123456789")

        # Create rooms
        room_type_simple = Room_type.objects.create(name="Simple", price=20, max_guests=1)
        room_type_double = Room_type.objects.create(name="Double", price=40, max_guests=2)
        room_type_triple = Room_type.objects.create(name="Triple", price=60, max_guests=3)
        cls.room_simple = Room.objects.create(room_type=room_type_simple, name="Room Simple", description="description simple")
        cls.room_double = Room.objects.create(room_type=room_type_double, name="Room Double", description="description doble")
        cls.room_triple = Room.objects.create(room_type=room_type_triple, name="Room Triple", description="description triple")

        # Make random date check in and checkout
        cls.check_in = date(2020, 1, 25)
        cls.check_out = date(2020, 1, 28)

        # Create bookings
        Booking.objects.create(
            checkin=cls.check_in,
            checkout=cls.check_out,
            room=cls.room_simple,
            guests=1,
            customer=cls.customer_1,
            total=20,
            code="1234"
        )

        Booking.objects.create(
            checkin=cls.check_in,
            checkout=cls.check_out,
            room=cls.room_double,
            guests=1,
            customer=cls.customer_1,
            total=20,
            code="1234"
        )

        Booking.objects.create(
            checkin=cls.check_in,
            checkout=cls.check_out,
            room=cls.room_double,
            guests=1,
            customer=cls.customer_1,
            total=20,
            code="1234",
            state=Booking.DELETED,
        )

        return super().setUpTestData()

    def test_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_url_resolves(self):
        view_class = resolve(self.url).func.view_class
        self.assertEqual(view_class, DashboardView)

    def test_template_name(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "dashboard.html")

    def test_context_data(self):
        response = self.client.get(self.url)
        dashboard = response.context["dashboard"]
        self.assertIn('new_bookings', dashboard)
        self.assertIn('incoming_guests', dashboard)
        self.assertIn('outcoming_guests', dashboard)
        self.assertIn('invoiced', dashboard)
        self.assertIn('occupancy_rate', dashboard)

    def test_new_bookings(self):
        response = self.client.get(self.url)

        today_min = datetime.combine(date.today(), time.min)
        today_max = datetime.combine(date.today(), time.max)

        expected = Booking.objects.filter(created__range=(today_min, today_max)).count()
        self.assertEqual(response.context["dashboard"]["new_bookings"], expected)

    def test_incoming_guests(self):
        with patch("pms.views.date") as mocked_date:
            mocked_date.today.return_value = self.check_in
            response = self.client.get(self.url)

        expected = Booking.objects.filter(checkin=self.check_in).exclude(state=Booking.DELETED).count()
        self.assertEqual(response.context["dashboard"]["incoming_guests"], expected)

    def test_outcoming_guests(self):
        with patch("pms.views.date") as mocked_date:
            mocked_date.today.return_value = self.check_out
            response = self.client.get(self.url)

        expected = Booking.objects.filter(checkout=self.check_out).exclude(state=Booking.DELETED).count()
        self.assertEqual(response.context["dashboard"]["outcoming_guests"], expected)

    def test_invoiced_guests(self):
        response = self.client.get(self.url)

        today_min = datetime.combine(date.today(), time.min)
        today_max = datetime.combine(date.today(), time.max)

        expected = Booking.objects.aggregate(
            total=Sum(
                "total", filter=Q(
                    Q(created__range=(today_min, today_max)) & ~Q(state=Booking.DELETED)
                )
            )
        )
        self.assertEqual(response.context["dashboard"]["invoiced"], expected["total"])

    def test_occupancy_rate(self):
        response = self.client.get(self.url)
        total_rooms = Room.objects.all().count()
        total_bookings = Booking.objects.filter(state=Booking.NEW).count()
        expected = round(total_bookings / total_rooms, 1) * 100

        self.assertEqual(response.context["dashboard"]["occupancy_rate"], expected)

    @patch('pms.views.Room.objects.all')
    def test_occupancy_rate_no_rooms(self, mocked_room):
        mocked_room.return_value.count.return_value = 0
        response = self.client.get(self.url)

        self.assertEqual(response.context["dashboard"]["occupancy_rate"], 0)
