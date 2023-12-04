from django.test import TestCase, Client
from django.urls import reverse

from .models import Room, Room_type, Booking, Customer
from .reservation_code import generate

class SetUp(TestCase):

    def setUp(self):
        """
        Setup:
        - 2 room types
        - 4 rooms
        - 2 customers
        - 2 bookings
        """
        simple_room_type = Room_type.objects.create(name='Simple', price=20.0, max_guests=1)
        double_room_type = Room_type.objects.create(name='Double', price=30.0, max_guests=2)

        room_1_1 = Room.objects.create(room_type=simple_room_type, name='Room 1.1', description='Lorem Ipsum')
        room_2_1 = Room.objects.create(room_type=double_room_type, name='Room 2.1', description='Lorem Ipsum')
        room_2_2 = Room.objects.create(room_type=double_room_type, name='Room 2.2', description='Lorem Ipsum')
        room_2_3 = Room.objects.create(room_type=double_room_type, name='Room 2.3', description='Lorem Ipsum')

        customer_1 = Customer.objects.create(name='Patricio Kumagae', email='kumagaepatricio@gmail.com',
                                             phone='123456789')
        customer_2 = Customer.objects.create(name='Chapp User', email='user@chapp.com',
                                             phone='123456789')

        booking_1 = Booking.objects.create(
            checkin='2023-12-01',
            checkout='2023-12-03',
            room=room_1_1,
            guests=1,
            customer=customer_1,
            total=40,
            code=generate.get()
        )

        booking_2 = Booking.objects.create(
            checkin='2023-12-04',
            checkout='2023-12-06',
            room=room_1_1,
            guests=1,
            customer=customer_2,
            total=40,
            code=generate.get()
        )

class TestDashboard(SetUp):

    def test_occupancy_percentage(self):
        """
        4 rooms and 2 bookings created on set up, should result as a 50% occupancy
        """

        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Occupancy percentage: 50.0 %')
