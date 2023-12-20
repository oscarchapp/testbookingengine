import unittest
from datetime import date
from django.test import TestCase
from django.urls import reverse
from .views import EditDateBookingView
from .models import Booking, Room, Room_type, Customer
from datetime import timedelta
from .reservation_code import generate
from .form_dates import Ymd
from django.db.models import F

class BookingSearchViewTest(TestCase):
    def setUp(self):
        self.customer1 = Customer.objects.create(name='Cliente 1', email='cliente1@example.com')
        self.customer2 = Customer.objects.create(name='Cliente 2', email='cliente2@example.com')
        self.booking1 = booking = Booking.objects.create(
            room=Room.objects.create(name='Habitación de prueba'),
            checkin=date.today(),
            checkout=date.today() + timedelta(days=2),
            guests=1, total=20
        )
        self.booking2 = booking = Booking.objects.create(
            room=Room.objects.create(name='Habitación de prueba 2'),
            checkin=date.today(),
            checkout=date.today() + timedelta(days=2),
            guests=2, total=30
        )

    def test_get_search_results_with_filter(self):
        response = self.client.get(reverse('booking_search') + '?filter=Cliente 1')
        self.assertEqual(response.status_code, 200)
        bookings = response.context['bookings']
        room_search_form = response.context['form']
        has_filter = response.context['filter']

        # Puedes agregar más afirmaciones según sea necesario

        # Verifica que la información de las reservas se muestra en el HTML
        for booking in bookings:
            self.assertContains(response, str(booking.code))
            self.assertContains(response, str(booking.customer.name))

    def test_get_search_results_without_filter(self):
        # Realiza la solicitud GET a la vista sin un filtro
        response = self.client.get(reverse('booking_search'))

        # Verifica que la respuesta redirige a la URL esperada (ajusta según tu aplicación)
        self.assertRedirects(response, '')


class RoomSearchViewTest(TestCase):
    def setUp(self):
        room_type1 = Room_type.objects.create(name='Tipo 1', price=20, max_guests=1)
        room_type2 = Room_type.objects.create(name='Tipo 2', price=30, max_guests=2)
        room_type3 = Room_type.objects.create(name='Tipo 3', price=40, max_guests=3)
        self.room1 = Room.objects.create(name='Habitación 1', room_type=room_type1)
        self.room2 = Room.objects.create(name='Habitación 2', room_type=room_type2)
        self.room3 = Room.objects.create(name='Habitación 3', room_type=room_type3)
        self.booking1 = booking = Booking.objects.create(
            room=Room.objects.create(name='Habitación de prueba'),
            checkin=date.today(),
            checkout=date.today() + timedelta(days=2),
            guests=1, total=20
        )
        self.booking2 = booking = Booking.objects.create(
            room=Room.objects.create(name='Habitación de prueba 2'),
            checkin=date.today(),
            checkout=date.today() + timedelta(days=2),
            guests=2, total=30
        )

    def test_get_search_form(self):
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)
        room_search_form = response.context['form']
        self.assertIsInstance(room_search_form, RoomSearchForm) 

    def test_post_search_results(self):
        post_data = {
            'checkin': str(date.today()+ timedelta(days=2)),
            'checkout': str(date.today() + timedelta(days=5)),
            'guests': '3',
        }
        response = self.client.post(reverse('search'), data=post_data)
        self.assertEqual(response.status_code, 200)
        rooms = response.context['rooms']
        total_rooms = response.context['total_rooms']
        query = response.context['query']
        url_query = response.context['url_query']
        data = response.context['data']
        for room in rooms:
            self.assertContains(response, str(room.name))
            self.assertContains(response, str(room.total)) 


class HomeViewTest(TestCase):
    def setUp(self):
        self.booking1 = booking = Booking.objects.create(
            room=Room.objects.create(name='Habitación de prueba'),
            checkin=date.today(),
            checkout=date.today() + timedelta(days=2),
            guests=1, total=20
        )
        self.booking2 = booking = Booking.objects.create(
            room=Room.objects.create(name='Habitación de prueba 2'),
            checkin=date.today(),
            checkout=date.today() + timedelta(days=2),
            guests=2, total=30
        )

    def test_get_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        bookings = response.context['bookings']
        self.assertQuerysetEqual(bookings, Booking.objects.all(), transform=lambda x: x)
        for booking in Booking.objects.all():
            self.assertContains(response, str(booking.total))



class DeleteBookingViewTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(name='Cliente de prueba', email='cliente@example.com')
        self.booking = Booking.objects.create(customer=self.customer,
            checkin=date.today(),
            checkout=date.today() + timedelta(days=2),
            guests=1, total=20
        )

    def test_get_delete_booking(self):
        response = self.client.get(reverse('delete_booking', args=[self.booking.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['booking'], self.booking)
        self.assertContains(response, str(self.booking.total))

    def test_post_delete_booking(self):
        response = self.client.post(reverse('delete_booking', args=[self.booking.id]))
        self.assertEqual(response.status_code, 302)


class EditBookingViewTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(name='Cliente de prueba', email='cliente@example.com')
        self.booking = Booking.objects.create(customer=self.customer,
            checkin=date.today(),
            checkout=date.today() + timedelta(days=2),
            guests=1, total=20
        )

    def test_get_edit_booking(self):
        response = self.client.get(reverse('edit_booking', args=[self.booking.id]))
        self.assertEqual(response.status_code, 200)
        booking_form = response.context['booking_form']
        customer_form = response.context['customer_form']
        self.assertEqual(booking_form.instance, self.booking)
        self.assertEqual(customer_form.instance, self.customer)
        self.assertContains(response, str(self.booking.total))
        self.assertContains(response, self.customer.name)

    #TODO: este marca error
    def test_post_update_customer(self):
        new_customer_data = {'name': 'Nuevo Nombre', 'email': 'nuevo_email@example.com'}
        response = self.client.post(reverse('edit_booking', args=[self.booking.id]), data=new_customer_data, prefix='customer')
        self.assertEqual(response.status_code, 302)
        self.booking.refresh_from_db()
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.name, new_customer_data['name'])
        self.assertEqual(self.customer.email, new_customer_data['email'])


class DashboardViewTest(TestCase):
    def setUp(self):
        self.room = Room.objects.create(name='Habitación de prueba')
        self.booking1 = booking = Booking.objects.create(
            room=Room.objects.create(name='Habitación de prueba'),
            checkin=date.today(),
            checkout=date.today() + timedelta(days=2),
            guests=1, total=20
        )
        self.booking2 = booking = Booking.objects.create(
            room=Room.objects.create(name='Habitación de prueba 2'),
            checkin=date.today(),
            checkout=date.today() + timedelta(days=2),
            guests=2, total=30
        )
    def test_get_dashboard(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        dashboard = response.context['dashboard']
        self.assertEqual(dashboard['new_bookings'], 1)
        self.assertEqual(dashboard['incoming_guests'], 1)
        self.assertEqual(dashboard['outcoming_guests'], 1)
        self.assertEqual(dashboard['invoiced']['total__sum'], Decimal('250.00'))
        self.assertEqual(dashboard['occupation'], 50)
        self.assertContains(response, str(dashboard['new_bookings']))
        self.assertContains(response, str(dashboard['incoming_guests']))
        self.assertContains(response, str(dashboard['outcoming_guests']))
        self.assertContains(response, str(dashboard['invoiced']['total__sum']))
        self.assertContains(response, str(dashboard['occupation']))


class RoomDetailsViewTest(TestCase):
    def setUp(self):
        self.room = Room.objects.create(name='Habitación de prueba')
        self.booking1 = booking = Booking.objects.create(
            room=Room.objects.create(name='Habitación de prueba'),
            checkin=date.today(),
            checkout=date.today() + timedelta(days=2),
            guests=1, total=20
        )
        self.booking2 = booking = Booking.objects.create(
            room=Room.objects.create(name='Habitación de prueba 2'),
            checkin=date.today(),
            checkout=date.today() + timedelta(days=2),
            guests=2, total=30
        )

    def test_get_room_details(self):
        response = self.client.get(reverse('room_details', args=[self.room.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['room'], self.room)
        self.assertQuerysetEqual(response.context['bookings'],
                                Booking.objects.filter(room=self.room),
                                transform=lambda x: x)

        self.assertContains(response, self.room.name)
        for booking in Booking.objects.filter(room=self.room):
            self.assertContains(response, str(booking.checkin))
            self.assertContains(response, str(booking.checkout))
            self.assertContains(response, str(booking.total))


class RoomsViewTest(TestCase):
    def setUp(self):
        room_type1 = Room_type.objects.create(name='Tipo 1', price=20, max_guests=4)
        room_type2 = Room_type.objects.create(name='Tipo 2', price=20, max_guests=4)
        Room.objects.create(name='Habitación 1', room_type=room_type1)
        Room.objects.create(name='Habitación 2', room_type=room_type2)

    def test_get_rooms(self):
        response = self.client.get(reverse('rooms'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['rooms'],
                                Room.objects.all(),
                                transform=lambda x: x)

        for room in Room.objects.all():
            self.assertContains(response, room.name)
            self.assertContains(response, room.room_type.name)


class EditDateBookingViewTest(TestCase):
    def setUp(self):
        self.booking = Booking.objects.create(checkin=date(2023, 1, 1), checkout=date(2023, 1, 5), guests=1, total=20)
    
    def test_get_method(self):
        try:
            response = self.client.get(reverse('edit_room', kwargs={'pk': self.booking.pk}))
            self.assertEqual(response.status_code, 200)
        except Exception as e:
            self.fail(f"Unexpected exception: {e}")

    def test_post_with_available_room(self):
        booking = Booking.objects.create(
            room=Room.objects.create(name='Habitación de prueba'),
            checkin=date.today(),
            checkout=date.today() + timedelta(days=2),
            guests=1, total=20
        )

        data = {'checkin': '2023-12-20', 'checkout': '2023-12-23'}
        response = self.client.post(reverse('edit_room', args=[booking.id]), data)
        self.assertEqual(response.status_code, 302)

    def test_post_with_unavailable_room(self):
        booking = Booking.objects.create(
            room=Room.objects.create(name='Habitación de prueba'),
            checkin=date.today(),
            checkout=date.today() + timedelta(days=2),
            guests=1, total=20
        )
        conflicting_booking = booking = Booking.objects.create(
            room=Room.objects.create(name='Habitación de prueba'),
            checkin=date.today(),
            checkout=date.today() + timedelta(days=2),
            guests=1, total=20
        )
        data = {'checkin': '2023-12-20', 'checkout': '2023-12-23'}
        response = self.client.post(reverse('edit_room', args=[booking.id]), data)
        self.assertEqual(response.status_code, 200)