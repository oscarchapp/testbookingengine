import email
from datetime import datetime, timedelta
from django.test import TestCase, Client

from .models import Room_type, Room, Customer, Booking


class TestOccupationDashboard(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client = Client()
        self.url = "/dashboard/"
    
    def test_occupation_no_rooms(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "0 %")
    
    def test_occupation_calculation(self) -> None:
        self.create_rooms_and_reservations()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "33 %")

    def create_rooms_and_reservations(self) -> None:
        test_room_type = Room_type.objects.create(
            name="test_type",
            price=10,
            max_guests=2
        )
        test_room=Room.objects.create(
            room_type=test_room_type,
            name="room 1.1",
            description="test room"
        )
        Room.objects.create(
            room_type=test_room_type,
            name="room 1.2",
            description="test room"
        )
        Room.objects.create(
            room_type=test_room_type,
            name="room 1.3",
            description="test room"
        )
        test_customer = Customer.objects.create(
            name="Pepito Perez",
            email="pepito.perez@gmail.com",
            phone="666666666"
        )
        Booking.objects.create(
            checkin=datetime(2022, 2, 11),
            checkout=datetime(2022, 2, 15),
            room=test_room,
            guests=2,
            customer=test_customer,
            total=30,
        )
