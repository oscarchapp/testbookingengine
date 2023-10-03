from django.test import TestCase
from django.urls import reverse
from pms.forms import BookingFormEdit
from pms.models import Booking, Room, Room_type, Customer
from datetime import date, time, datetime
from django.db.models import Sum

# Create your tests here.
class BaseTestCase(TestCase):
  def setUp(self):
    Single = Room_type.objects.create(name="Single", price=1000, max_guests=1)
    Doble = Room_type.objects.create(name="Doble", price=2000, max_guests=1)
    Triple = Room_type.objects.create(name="Triple", price=3000, max_guests=1)
    Cuadruple = Room_type.objects.create(name="Cuádruple", price=4000, max_guests=1)

    # create models rooms
    self.room1 = Room.objects.create(name="Room 1.1", room_type=Single)
    self.room2 = Room.objects.create(name="Room 1.2", room_type=Single)
    self.room3 = Room.objects.create(name="Room 1.3", room_type=Single)
    self.room4 = Room.objects.create(name="Room 2.1", room_type=Doble)
    self.room5 = Room.objects.create(name="Room 2.2", room_type=Doble)
    self.room6 = Room.objects.create(name="Room 2.3", room_type=Doble)
    self.room7 = Room.objects.create(name="Room 3.1", room_type=Triple)
    self.room8 = Room.objects.create(name="Room 3.2", room_type=Triple)
    self.room9 = Room.objects.create(name="Room 3.3", room_type=Triple)
    self.room10 = Room.objects.create(name="Room 4.1", room_type=Cuadruple)
    self.room11 = Room.objects.create(name="Room 4.2", room_type=Cuadruple)

    # create models customers
    self.customer1 = Customer.objects.create(
      name="John Doe",
      email="jhon@gmail.com",
      phone="123456789"
    )
    self.customer2 = Customer.objects.create(
      name="Carlos Acosta",
      email="carlos@gmail.com",
      phone="123456789"
    )

    # create models bookings
    self.booking = Booking.objects.create(
      checkin="2023-10-02",
      checkout="2023-10-10",
      room=self.room1,
      guests=3,
      customer=self.customer1,
      total=90.0,
      code="ABC123",
      state="NEW"
    )

    self.booking1 = Booking.objects.create(
      checkin="2023-10-02",
      checkout="2023-10-10",
      room=self.room1,
      guests=1,
      customer=self.customer1,
      total=30.0,
      code="ABC123",
      state="NEW"
    )
    
    self.booking2 = Booking.objects.create(
      checkin="2023-10-04",
      checkout="2023-10-08",
      room=self.room1,
      guests=1,
      customer=self.customer2,
      total=20.0,
      code="ABC123",
      state="NEW"
    )

    self.booking3 = Booking.objects.create(
      checkin="2023-10-04",
      checkout="2023-10-08",
      room=self.room1,
      guests=1,
      customer=self.customer2,
      total=60.0,
      code="ABC123",
      state="DEL"
    )

    self.today = date.today()
    self.today_min = datetime.combine(self.today, time.min)
    self.today_max = datetime.combine(self.today, time.max)
    self.today_range = (self.today_min, self.today_max)

    self.booking3 = Booking.objects.create(
      checkin=self.today,
      checkout=self.today,
      room=self.room1,
      guests=1,
      customer=self.customer2,
      total=20.0,
      code="ABC123",
      state="DEL"
    )

# ./manage.py test pms.tests.UpdateBookingViewTestCase
class UpdateBookingViewTestCase(BaseTestCase):
  def setUp(self):
    return super().setUp()
  
  # ./manage.py test pms.tests.UpdateBookingViewTestCase.test_get_valid_booking
  def test_get_valid_booking(self):
    url = reverse('update_booking', args=[self.booking.pk])
    response = self.client.get(url)
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'update_booking.html')
    self.assertIsInstance(response.context['booking_form'], BookingFormEdit)

  # ./manage.py test pms.tests.UpdateBookingViewTestCase.test_get_invalid_booking
  def test_get_invalid_booking(self):
    url = reverse('update_booking', args=[999])
    response = self.client.get(url)
    # booking not found and redirect
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, '/')
  
  # ./manage.py test pms.tests.UpdateBookingViewTestCase.test_get_invalid_booking_state
  def test_get_invalid_booking_state(self):
    url = reverse('update_booking', args=[self.booking3.pk])
    response = self.client.get(url)
    # booking state invalid and redirect
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, '/')

  # ./manage.py test pms.tests.UpdateBookingViewTestCase.test_post_valid_data
  def test_post_valid_edit(self):
      url = reverse('update_booking', args=[self.booking1.pk])
      # update booking successfully
      data = {
          'booking-checkin': '2023-12-01',
          'booking-checkout': '2023-12-05',
      }
      response = self.client.post(url, data)

      # assert redirect
      self.assertEqual(response.status_code, 302)
      self.assertRedirects(response, '/')

  # ./manage.py test pms.tests.UpdateBookingViewTestCase.test_post_invalid_edit
  def test_post_invalid_edit(self):
    url = reverse('update_booking', args=[self.booking.pk])
    data = {
        'booking-checkin': '2023-10-03',
        'booking-checkout': '2023-10-10',
    }
    response = self.client.post(url, data)
    # assert not update, not disponibility
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'update_booking.html')
    self.assertIn('error_message', response.context)

  # ./manage.py test pms.tests.UpdateBookingViewTestCase.test_post_invalid_booking
  def test_post_invalid_booking(self):
    url = reverse('update_booking', args=[999])
    data = {
        'booking-checkin': '2023-12-01',
        'booking-checkout': '2023-12-05',
    }
    response = self.client.post(url, data)
    # booking not found and redirect
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, '/') 

  # ./manage.py test pms.tests.UpdateBookingViewTestCase.test_post_invalid_booking_state
  def test_post_invalid_booking_state(self):
    url = reverse('update_booking', args=[self.booking3.pk])
    data = {
        'booking-checkin': '2023-12-01',
        'booking-checkout': '2023-12-05',
    }
    response = self.client.post(url, data)
    # booking state invalid and redirect
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, '/')