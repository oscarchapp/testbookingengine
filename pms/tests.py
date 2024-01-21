from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client

# Create your tests here.

from django.urls import reverse
from datetime import date, timedelta
from .models import Booking, Room, Room_type, Customer
from .views import EditBookingView

class EditBookingViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.room_type = Room_type.objects.create(name='Single', price=100, max_guests=1)
        self.room = Room.objects.create(room_type=self.room_type, name='1.1', description='Habitación individual')
        self.customer = Customer.objects.create(name='Test Customer', email='customer@mail.com', phone='123456789')
        self.booking = Booking.objects.create(
            state=Booking.NEW,
            checkin=date.today(),
            checkout=date.today() + timedelta(days=2),
            room=self.room,
            guests=1,
            customer=self.customer,
            total=200,
            code='ABC123'
        )

    def test_edit_booking_view_get(self):
        response = self.client.get(reverse('edit_booking', kwargs={'pk': self.booking.id, 'edit_type': 'date'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Editar fechas de reserva')
        self.assertContains(response, 'Guardar datos')

    # TODO
    ## Due to lack of time I would just propose some more test, like mock the post form for both failure & success