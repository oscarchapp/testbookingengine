from django.test import TestCase
from django.urls import reverse
from datetime import date, timedelta

from .models import Customer, Room_type, Room, Booking
from .forms import BookingEditForm

class EditReservationViewTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(name='Test Customer', email='test@example.com', phone='1234567890')
        self.room_type = Room_type.objects.create(name='Test Room Type', price=100, max_guests=2)
        self.room = Room.objects.create(room_type=self.room_type, name='Test Room', description='Test Room Description')
        self.booking = Booking.objects.create(state=Booking.NEW, checkin=date.today(), checkout=date.today() + timedelta(days=1), room=self.room, guests=2, customer=self.customer, total=100, code='ABC123')

    def test_get_edit_reservation_view(self):
        url = reverse('edit_reservation', args=[self.booking.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Editar reserva')

    def test_post_valid_edit_reservation_view(self):
        url = reverse('edit_reservation', args=[self.booking.pk])
        new_checkin = date.today() + timedelta(days=2)
        new_checkout = date.today() + timedelta(days=3)
        data = {'checkin': new_checkin, 'checkout': new_checkout}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        updated_booking = Booking.objects.get(pk=self.booking.pk)
        self.assertEqual(updated_booking.checkin, new_checkin)
        self.assertEqual(updated_booking.checkout, new_checkout)

    def test_post_invalid_edit_reservation_view(self):
        url = reverse('edit_reservation', args=[self.booking.pk])
        data = {'checkin': date.today(), 'checkout': date.today() + timedelta(days=2)}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

    def test_clean_checkin_greater_than_checkout(self):
        data = {'checkin': date.today() + timedelta(days=2), 'checkout': date.today() + timedelta(days=1)}
        form = BookingEditForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('Fecha de Checkin debe ser menor a fecha de Checkout.', form.errors['__all__'])

