from django.test import TestCase
from django.urls import reverse
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

# ./manage.py test pms.tests.RoomsViewTestCase
class RoomsViewTestCase(BaseTestCase):
  def setUp(self):
    return super().setUp()    

  def compare_querysets(self, query1, query2):
    query1_values = [str(item.get('name')) for item in query1]
    query2_values = [str(item.name) for item in query2]
    self.assertListEqual(query1_values, query2_values)

  # ./manage.py test pms.tests.RoomsViewTestCase.test_rooms_view_all
  def test_rooms_view_all(self):
    response = self.client.get(reverse('rooms'))
    self.assertEqual(response.status_code, 200)
    queryset = response.context['rooms']

    # assert quantity of rooms
    self.assertEqual(queryset.count(), 11)

    # filter rooms
    filtered_rooms = Room.objects.all()

    # assert rooms are the same
    self.compare_querysets(queryset, filtered_rooms)

  # ./manage.py test pms.tests.RoomsViewTestCase.test_rooms_view_valid_filter
  def test_rooms_view_valid_filter(self):
    response = self.client.get(reverse('rooms'), {'search_room': 'Room 1'})
    self.assertEqual(response.status_code, 200)
    queryset = response.context['rooms']
    # assert quantity of rooms
    self.assertEqual(queryset.count(), 3)

    filtered_rooms = Room.objects.filter(name__startswith='Room 1')

    # assert rooms are the same
    self.compare_querysets(queryset, filtered_rooms)

  # ./manage.py test pms.tests.RoomsViewTestCase.test_rooms_view_invalid_filter
  def test_rooms_view_invalid_filter(self):
    response = self.client.get(reverse('rooms'), {'search_room': 'asdasdsa'})
    self.assertEqual(response.status_code, 200)
    queryset = response.context['rooms']

    # assert quantity of rooms
    self.assertEqual(queryset.count(), 0)
    # assert empty queryset
    self.assertQuerysetEqual(queryset, [])