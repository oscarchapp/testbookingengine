from datetime import date

from django.test import TestCase

from pms.models import Booking, Room, Customer, Room_type


# Create your tests here.
class BookingTestCase(TestCase):

    def setUp(self):
        self.room_type = Room_type.objects.create(
            name="Simple",
            price=10.50,
            max_guests=1
        )
        self.room = Room.objects.create(
            room_type=self.room_type,
            name="Habitación 1",
            description="Habitación para una persona"
        )
        self.customer = Customer.objects.create(
            name="Javier",
            email="javier@prueba.com",
            phone="654654654"
        )
        self.booking = Booking.objects.create(
            state="NEW",
            checkin=date.today(),
            checkout=date.today(),
            room=self.room,
            guests=1,
            customer=self.customer,
            total=1,
            code=1,
            created=date.today()
        )

    # Test to check room type creation
    def test_create_room_type(self):
        self.assertEqual(self.room_type.name, "Simple")
        self.assertEqual(self.room_type.price, 10.50)
        self.assertEqual(self.room_type.max_guests, 1)

    # Test to check room creation
    def test_create_room(self):
        self.assertEqual(self.room.room_type, self.room_type)
        self.assertEqual(self.room.name, "Habitación 1")
        self.assertEqual(self.room.description, "Habitación para una persona")

    # Test to check customer creation
    def test_create_customer(self):
        self.assertEqual(self.customer.name, "Javier")
        self.assertEqual(self.customer.email, "javier@prueba.com")
        self.assertEqual(self.customer.phone, "654654654")

    # Test to check booking creation
    def test_create_booking(self):
        self.assertEqual(self.booking.id, 1)
        self.assertEqual(self.booking.state, "NEW")
        self.assertEqual(self.booking.room, self.room)
        self.assertEqual(self.booking.customer, self.customer)

    # Test to check booking update
    def test_booking_update(self):
        room_type = Room_type.objects.create(
            name="Double",
            price=21.00,
            max_guests=2
        )
        room = Room.objects.create(
            room_type=room_type,
            name="Habitación 2",
            description="Habitación para dos persona"
        )
        self.booking.room = room
        self.booking.state = 'DEL'
        self.booking.guests = '4'
        self.booking.save()
        self.assertEqual(self.booking.state, 'DEL')
        self.assertEqual(self.booking.room, room)
