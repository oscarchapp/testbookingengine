from django.test import TestCase
from datetime import datetime, timedelta
from .models import Room, Booking

class OccupancyRateTestCase(TestCase):
    def setUp(self):
        room1 = Room.objects.create(name="Room 1",description="Room number 1")
        room1_2 = Room.objects.create(name="Room 1.2",description="Room number 1.2")
        room2= Room.objects.create(name="Room 2",description="Room number 2")
        Booking.objects.create(checkin=datetime.today(),checkout = datetime.today() + timedelta(days=2),room=room1,guests=1,total=30)
        Booking.objects.create(checkin=datetime.today(),checkout = datetime.today() + timedelta(days=3),room=room1_2,guests=1,total=50)
        Booking.objects.create(checkin=datetime.today(),checkout = datetime.today() + timedelta(days=3),room=room2,guests=2,total=20)

    def test_get_room_by_name_correctly(self):
        room1 = Room.objects.get(name="Room 1")
        self.assertEqual(room1.description, "Room number 1")
        self.assertFalse(Room.objects.filter(name="NoExiste").exists())

    def test_get_room_by_description_correctly(self):
        room1 = Room.objects.get(description="Room number 1")
        self.assertEqual(room1.name, "Room 1")
        self.assertFalse(Room.objects.filter(description="NoExiste").exists())

    def test_get_booking_by_checkin_correctly(self):
        booking = Booking.objects.filter(checkin=datetime.today())
        self.assertEqual(booking.count(), 3)
        self.assertFalse(Booking.objects.filter(checkin=datetime.today() - timedelta(days=1)).exists())
    
    def test_get_booking_by_checkout_correctly(self):
        booking = Booking.objects.filter(checkout = datetime.today() + timedelta(days=2))
        self.assertEqual(booking.count(), 1)
        self.assertFalse(Booking.objects.filter(checkout=datetime.today() - timedelta(days=1)).exists())

    def test_get_booking_by_guestscorrectly(self):
        room1 = Room.objects.get(name="Room 1")
        booking = Booking.objects.filter(room=room1)
        self.assertEqual(booking.count(), 1)

    def test_get_booking_by_guests_correctly(self):
        booking = Booking.objects.filter(guests=1)
        self.assertEqual(booking.count(), 2)
        self.assertFalse(Booking.objects.filter(guests=5).exists())

    def test_get_booking_by_total_correctly(self):
        booking = Booking.objects.filter(total=30)
        self.assertEqual(booking.count(), 1)
        self.assertFalse(Booking.objects.filter(total=0).exists())

    #test that represents the second requirement
    def test_occupancy_rate(self):
        rooms = (Room.objects.all()).count()
        confirmed_bookings = (Booking.objects.filter(state='NEW').values("room").distinct()).count()
        self.assertEqual(rooms,3)
        self.assertEqual(confirmed_bookings,3)
        #expect 100% occupancy 
        self.assertEqual((confirmed_bookings/rooms)*100,100)
        #created a new room
        room3= Room.objects.create(name="Room 3",description="Room number 3")
        rooms = (Room.objects.all()).count()
        confirmed_bookings = (Booking.objects.filter(state='NEW').values("room").distinct()).count()
        self.assertEqual(rooms,4)
        self.assertEqual(confirmed_bookings,3)
        #expect 75% occupancy 
        self.assertEqual((confirmed_bookings/rooms)*100,75)
        #created a room reservation with a room with reservation
        room1 = Room.objects.get(name="Room 1")
        Booking.objects.create(checkin=datetime.today()+ timedelta(days=7),checkout = datetime.today() + timedelta(days=8),room=room1,guests=2,total=20)
        rooms = (Room.objects.all()).count()
        confirmed_bookings = (Booking.objects.filter(state='NEW').values("room").distinct()).count()
        #expect 75% occupancy 
        self.assertEqual(rooms,4)
        self.assertEqual(confirmed_bookings,3)
        self.assertEqual((confirmed_bookings/rooms)*100,75)
        #booked the new room
        Booking.objects.create(checkin=datetime.today()+ timedelta(days=7),checkout = datetime.today() + timedelta(days=8),room=room3,guests=2,total=20)
        rooms = (Room.objects.all()).count()
        confirmed_bookings = (Booking.objects.filter(state='NEW').values("room").distinct()).count()
        #expect 100% occupancy 
        self.assertEqual(rooms,4)
        self.assertEqual(confirmed_bookings,4)
        self.assertEqual((confirmed_bookings/rooms)*100,100)