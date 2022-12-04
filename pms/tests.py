from django.test import TestCase, Client
from .models import Room, Room_type, Booking, Customer

class BookingTestCase(TestCase):

    def setUp(self):
        self.roomtype_simple = Room_type.objects.create(name = "Simple",price = 20,max_guests = 1)
        self.room_simple = Room.objects.create(room_type = self.roomtype_simple,name = "Room 1.1",description = "Testing room simple")

        self.customer_1 = Customer.objects.create(name='Nick', email='nick_test@email.com',phone='933656789')
        self.customer_2 = Customer.objects.create(name='Eva', email='eva_test@email.com',phone='933656786')
        self.booking_1 = Booking.objects.create(checkin = '2022-11-01',checkout = '2022-11-10',room = self.room_simple,guests = 1,customer = self.customer_1,total = 200,code = 'WDEFTX8HB')
        self.booking_2 = Booking.objects.create(checkin = '2022-11-11',checkout = '2022-11-20',room = self.room_simple,guests = 1,customer = self.customer_2,total = 200,code = 'WDZFTX8HC')

    def test_confict_rangedates_edit_booking(self):
        data = {'checkin': '2022-11-09', 'checkout': '2022-10-13'}
        response = self.client.post('/booking/'+str(self.booking_1.id)+'/edit-date', data)
        error = "".join(list(response.context['error']))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(error, 'La fecha de Checkin no puede ser despues de checkout')

    
    def test_confict_save_edit_booking(self):
        data = {'checkin': '2022-11-05', 'checkout': '2022-11-15'}
        response = self.client.post('/booking/'+str(self.booking_1.id)+'/edit-date', data)
        error = "".join(list(response.context['error']))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(error, 'No hay disponibilidad para las fechas seleccionadas')


    def test_save_edit_booking(self):
        data = {'checkin': '2022-11-21', 'checkout': '2022-11-25'}
        response = self.client.post('/booking/'+str(self.booking_1.id)+'/edit-date', data)
        booking = Booking.objects.filter(id=self.booking_1.id).values("checkin","checkout")
        checkin = str(list(booking)[0]['checkin'])
        checkout = str(list(booking)[0]['checkout'])

        self.assertEqual(response.status_code, 302)
        self.assertEqual(data['checkin'], checkin)
        self.assertEqual(data['checkout'], checkout)
