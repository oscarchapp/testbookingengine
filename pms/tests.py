from django.test import TestCase
from pms.models import (Room,Customer,Room_type,Booking)

# Create your tests here.
# RUN TEST ./manage.py test pms.tests.TestCases

class TestCases(TestCase):
    def setUp(self):
        self.roomType = Room_type.objects.create(name = "Simple",price = 20,max_guests = 1)
        self.room = Room.objects.create(room_type= self.roomType,name = "Room 1.1",description = "Room 1.1")
        self.room2 = Room.objects.create(room_type= self.roomType,name = "Room 1.2",description = "Room 1.2")
        self.customer = Customer.objects.create(name='Guadalupe', email='test@hotmail.com',phone='2289436253')
        self.customer2 = Customer.objects.create(name='Renata', email='test@hotmail.com',phone='2239436253')
        self.booking = Booking.objects.create(checkin = '2022-11-19',checkout = '2022-11-21',room = self.room,guests = 1,customer = self.customer,total = 40,code = 'CVMGTH345')
        self.booking2 = Booking.objects.create(checkin = '2022-11-23',checkout = '2022-11-24',room = self.room2,guests = 1,customer = self.customer2,total = 40,code = 'CM65TH345')
    
    def test_filter_byname(self):
        data = {'name':'Room 1'}
        self.assertIsNotNone(Room.objects.filter(name__icontains=data.get('name')))