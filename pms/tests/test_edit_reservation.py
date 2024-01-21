from django.test import TestCase, RequestFactory
from django.urls import reverse
from datetime import date, timedelta
from pms.models import Booking, Room, Room_type, Customer
from pms.views import EditReservationView

class EditReservationViewTest(TestCase):
    def setUp(self):
        # setup rooms and booking
        room_type = Room_type.objects.create(name='Single', price=50.0, max_guests=1)
        self.room = Room.objects.create(room_type=room_type, name='Room 1.1', description='Single Room')
        customer = Customer.objects.create(name='Dharma Alisum', email='dharma@test.com', phone='123456789')
        self.booking = Booking.objects.create(
            state='NEW',
            checkin=date.today(),
            checkout=date.today() + timedelta(days=1),
            room=self.room,
            guests=1,
            customer=customer,
            total=50.0,
            code='ABC123'
        )

        self.booking2 = Booking.objects.create(
            state='NEW',
            checkin=date.today()+ timedelta(days=5),
            checkout=date.today() + timedelta(days=6),
            room=self.room,
            guests=1,
            customer=customer,
            total=50.0,
            code='ABC123'
        )

    def test_get_method(self):

        response = self.client.get(reverse('edit_reservation', kwargs={'pk': self.booking.id}))

        # response verify
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<h2>Edit Reservation</h2>')

        # verify valid form
        form = response.context['form']
        self.assertEqual(form.instance, self.booking)

    def test_post_method_valid_form(self):
        # test POST with valid form
        new_checkin = date.today() + timedelta(days=2)
        new_checkout = date.today() + timedelta(days=3)
        data = {
            'checkin': new_checkin,
            'checkout': new_checkout,
        }
        response = self.client.post(reverse('edit_reservation', kwargs={'pk': self.booking.id}), data)

        # redirect verify
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

        # verify changes in db
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.checkin, new_checkin)
        self.assertEqual(self.booking.checkout, new_checkout)

    def test_post_method_invalid_form(self):
        # test POST with invalid form
        new_checkin = date.today() + timedelta(days=5)
        new_checkout = date.today() + timedelta(days=6)
        data = {
            'checkin': new_checkin,
            'checkout': new_checkout,
        }
        response = self.client.post(reverse('edit_reservation', kwargs={'pk': self.booking.id}), data)

         # Verify status code & error message
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No hay disponibilidad para las fechas seleccionadas.')

        # Verify data in db not changed
        self.booking.refresh_from_db()
        self.assertNotEqual(self.booking.checkin, new_checkin)
        self.assertNotEqual(self.booking.checkout, new_checkout)
