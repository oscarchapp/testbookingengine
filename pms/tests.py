from django.test import TestCase, Client
from django.urls import reverse

from .models import Room, Room_type, Booking, Customer
from .reservation_code import generate


class SetUp(TestCase):

    def setUp(self):
        """"
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


class TestBookings(SetUp):

    def test_edit_booking_dates_unavailable_room(self):
        """
        Testing unavailable dates
        Trying to modify dates from booking 2, with same dates as booking 1
        """
        booking_1 = Booking.objects.filter(customer__name='Patricio Kumagae').first()
        booking_2 = Booking.objects.filter(customer__name='Chapp User').first()

        response = self.client.post(reverse('edit_booking_dates', args=[booking_2.id]), data={'checkin': str(booking_1.checkin), 'checkout': str(booking_1.checkout)})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No hay disponibilidad para las fechas seleccionadas')

    def test_edit_booking_dates_available_room(self):
        """
        Testing available dates
        """
        booking_1 = Booking.objects.filter(customer__name='Patricio Kumagae').first()

        response = self.client.post(reverse('edit_booking_dates', args=[booking_1.id]), data={'checkin': '2023-12-15', 'checkout': '2023-12-17'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Fechas modificadas')

    def test_edit_booking_dates_same_day_checkin_checkout(self):
        """
        Testing booking 2 checkin date equals booking 1 checkout date
        """
        booking_1 = Booking.objects.filter(customer__name='Patricio Kumagae').first()
        booking_2 = Booking.objects.filter(customer__name='Chapp User').first()

        response = self.client.post(reverse('edit_booking_dates', args=[booking_2.id]), data={'checkin': str(booking_1.checkout), 'checkout': str(booking_2.checkout)})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Fechas modificadas')

    def test_edit_booking_dates_invalid_dates(self):
        """
        Testing checkout date < checkin date
        """
        booking_1 = Booking.objects.filter(customer__name='Patricio Kumagae').first()

        response = self.client.post(reverse('edit_booking_dates', args=[booking_1.id]), data={'checkin': '2023-12-15', 'checkout': '2023-12-14'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'La fecha del checkout debe ser mayor a la del checkin')

    def test_edit_booking_dates_invalid_booking_params(self):
        """
        Testing with booking ID 8 which does not exist
        """

        response = self.client.post(reverse('edit_booking_dates', args=[8]), data={'checkin': '2023-12-15', 'checkout': '2023-12-14'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ocurrió un error al intentar modificar las fechas')

    def test_edit_booking_dates_invalid_booking_dates(self):
        """
        Testing with checkin date 'abc' which is not a valid date
        """

        booking_1 = Booking.objects.filter(customer__name='Patricio Kumagae').first()

        response = self.client.post(reverse('edit_booking_dates', args=[booking_1.id]), data={'checkin': 'abc', 'checkout': '2023-12-14'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ocurrió un error al intentar modificar las fechas')
