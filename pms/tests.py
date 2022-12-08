from django.test import TestCase, Client
from pms.models import Room, Booking
import datetime
from decimal import Decimal
import uuid
from django.urls import reverse
from pms.forms import BookingEditForm

class RoomsViewTest(TestCase):
    def setUp(self):
        rooms = [
            Room(
                name='room 1.1',
                description='Room description test'
            ),
            Room(
                name='room 2',
                description='Room description test'
            ),
            Room(
                name='room 2.2',
                description='Room description test'
            )
        ]
        Room.objects.bulk_create(rooms)
        self.client = Client()

    def test_search_name_room(self):
        data = {'name': 'room 1'}
        res = self.client.post('/rooms/', data)
        self.assertEqual(len(res.context['rooms']), 1)
        self.assertEqual(res.status_code, 200)


class DashboardViewTest(TestCase):

    def setUp(self):
        rooms = [
            Room(
                name='room 1.1',
                description='Room description test'
            ),
            Room(
                name='room 2',
                description='Room description test'
            ),
            Room(
                name='room 2.2',
                description='Room description test'
            )
        ]

        Room.objects.bulk_create(rooms)
            
        booking = [
            Booking(
                state=Booking.COMFIRMED,
                checkin=datetime.datetime.now().date(),
                checkout=datetime.datetime.now().date(),
                room_id=1,
                guests=3,
                total=Decimal(40.0),
                code=uuid.uuid4().hex[:8]
            ),
            Booking(
                state=Booking.COMFIRMED,
                checkin=datetime.datetime.now().date(),
                checkout=datetime.datetime.now().date(),
                room_id=2,
                guests=3,
                total=Decimal(30.0),
                code=uuid.uuid4().hex[:8]
            ),
            Booking(
                state=Booking.COMFIRMED,
                checkin=datetime.datetime.now().date(),
                checkout=datetime.datetime.now().date(),
                room_id=3,
                guests=3,
                total=Decimal(10.0),
                code=uuid.uuid4().hex[:8]
            )
        ]
        Booking.objects.bulk_create(booking)
        self.client = Client()

    def test_percentage_occupied_rooms(self):
        response = self.client.get(reverse('dashboard'))
        content = response.context['dashboard']
        self.assertAlmostEqual(content['occupancy_rate'], 100)

class EditBookingViewTest(TestCase):

    def setUp(self):
        rooms = [
            Room(
                name='room 1.1',
                description='Room description test'
            ),
            Room(
                name='room 2',
                description='Room description test'
            ),
            Room(
                name='room 2.2',
                description='Room description test'
            )
        ]

        Room.objects.bulk_create(rooms)
            
        booking = [
            Booking(
                state=Booking.COMFIRMED,
                checkin=datetime.date(2022,12,8),
                checkout=datetime.date(2022,12,9),
                room_id=1,
                guests=3,
                total=Decimal(40.0),
                code=uuid.uuid4().hex[:8]
            ),
            Booking(
                state=Booking.COMFIRMED,
                checkin=datetime.date(2022,12,10),
                checkout=datetime.date(2022,12,11),
                room_id=1,
                guests=3,
                total=Decimal(30.0),
                code=uuid.uuid4().hex[:8]
            )]
        Booking.objects.bulk_create(booking)
        self.client = Client()
    
    def test_invalid_date_edit(self):
        form_data = {"checkin": datetime.date(2022,12,9), "checkout": datetime.date(2022,12,11)}
        form = BookingEditForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue('No hay disponibilidad para las fechas seleccionadas' in form.non_field_errors())
    
    def test_valid_date_edit(self):
        form_data = {"checkin": datetime.date(2022,12,12), "checkout": datetime.date(2022,12,11)}
        form = BookingEditForm(data=form_data)
        self.assertTrue(form.is_valid())


