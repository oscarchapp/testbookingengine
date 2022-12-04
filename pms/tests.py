from django.test import TestCase

from django.test import TestCase, Client
from .models import Room, Booking, Customer, Room_type
from datetime import datetime, timedelta
from django.utils import timezone

class RoomTestCase(TestCase):
    def setUp(self):
        self.client = Client(HTTP_USER_AGENT='Mozilla/6.0')
        self.today_range = (datetime.now(),datetime.now() + timedelta(days=1))
        
        self.roomtype_simple = Room_type.objects.create(name = "Simple",price = 20,max_guests = 1)
        self.roomtype_doble = Room_type.objects.create(name = "Doble",price = 30,max_guests = 2)
        self.roomtype_triple = Room_type.objects.create(name = "Triple",price = 40,max_guests = 3)

        self.room_simple_1 = Room.objects.create(room_type = self.roomtype_simple,name = "Room 1.1",description = "Disponible")
        self.room_simple_2 = Room.objects.create(room_type = self.roomtype_simple,name = "Room 1.2",description = "Disponible")
        self.room_doble = Room.objects.create(room_type = self.roomtype_doble,name = "Room 2.1",description = "Disponible")
        self.room_triple = Room.objects.create(room_type = self.roomtype_triple,name = "Room 3.1",description = "Disponible")

        Customer.objects.create(name="Test", email="test@test.es", phone="123456789").save()

        Booking.objects.create(state="NEW",
            checkin = self.today_range[0],
            checkout = self.today_range[1],
            room = Room.objects.get(name="Room 1.1"),
            guests = 1,
            customer = Customer.objects.get(name="Test"),
            total = 100.0 ,
            code = 'AB123456',
            created = datetime.now(),        
        ).save()

        Booking.objects.create(state="NEW",
            checkin = self.today_range[0],
            checkout = self.today_range[1],
            room = Room.objects.get(name="Room 2.1"),
            guests = 1,
            customer = Customer.objects.get(name="Test"),
            total = 100.0 ,
            code = 'AB123457',
            created = datetime.now(),        
        ).save()
    
    def test_search_room(self):
        response = self.client.get('/dashboard/')
        dashboard = list(response.context['dashboard'].values())
        new_bookings = dashboard[0]
        incoming = dashboard[1]
        outcoming = dashboard[2]
        percentage_occupation = dashboard[3]
        invoiced = dashboard[4]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(new_bookings,2)
        self.assertEqual(incoming,2)
        self.assertEqual(outcoming,0)
        self.assertEqual(percentage_occupation,50.0)
        self.assertEqual(invoiced['total__sum'],200.0)

