from django.test import TestCase

# Create your tests here.
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

# ./manage.py test pms.tests.DashboardViewTestCase
class DashboardViewTestCase(BaseTestCase):
  def setUp(self):
    return super().setUp()
  
  def get_data_dashboard(self):
    
    # get bookings created today
    new_bookings = (Booking.objects
                .filter(created__range=self.today_range)
                .values("id")
                ).count()
    
    # get incoming guests
    incoming = (Booking.objects
                .filter(checkin=self.today)
                .exclude(state="DEL")
                .values("id")
                ).count()

    # get outcoming guests
    outcoming = (Booking.objects
                  .filter(checkout=self.today)
                  .exclude(state="DEL")
                  .values("id")
                  ).count()

    # get outcoming guests
    invoiced = (Booking.objects
                .filter(created__range=self.today_range)
                .exclude(state="DEL")
                .aggregate(Sum('total'))
                )

    # get occupancy percentage
    booking_confirmed, rooms = (
                Booking.objects.filter(state="NEW").count(), 
                Room.objects.all().count()
                )
  
    return {
      'new_bookings': new_bookings,
      'incoming_guests': incoming,
      'outcoming_guests': outcoming,
      'invoiced': invoiced.get('total__sum', 0),
      'occupancy_percentage': booking_confirmed / rooms * 100 if rooms > 0 else 0
    }
  
  # ./manage.py test pms.tests.DashboardViewTestCase.test_dashboard_view
  def test_dashboard_view(self):
    response = self.client.get(reverse('dashboard'))

    # 200 OK status code
    self.assertEqual(response.status_code, 200)
    dashboard = response.context['dashboard']

    dashboard_data = self.get_data_dashboard()

    # assert dashboard data
    self.assertEqual(dashboard['new_bookings'], dashboard_data.get('new_bookings'))
    self.assertEquals(dashboard['incoming_guests'], dashboard_data.get('incoming_guests'))
    self.assertEquals(dashboard['outcoming_guests'], dashboard_data.get('outcoming_guests'))
    self.assertEquals(dashboard['invoiced']['total__sum'], dashboard_data.get('invoiced'))
    self.assertEquals(dashboard['occupancy_percentage'],dashboard_data.get('occupancy_percentage'))

    # template used
    self.assertTemplateUsed(response, 'dashboard.html')